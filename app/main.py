from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from app.schema import UserCreateSchema
from app.services import get_users, create_user

app = FastAPI(title="FastAPI Docker Test with Monitoring")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'fastapi_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'fastapi_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

USERS_COUNT = Gauge(
    'fastapi_users_total',
    'Total number of users in the system'
)

# Middleware to track metrics
@app.middleware("http")
async def prometheus_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

@app.get("/")
def index():
    return {"message": "Hello from FastAPI with Prometheus Monitoring! 📊"}

@app.get("/users")
def read_users():
    users = get_users()
    USERS_COUNT.set(len(users))
    return {"data": users}

@app.post("/users")
def add_user(user: UserCreateSchema):
    create_user(user.dict())
    users = get_users()
    USERS_COUNT.set(len(users))
    return {"success": True}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}
