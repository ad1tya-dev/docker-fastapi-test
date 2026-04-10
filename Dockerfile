FROM python:3.9-slim

WORKDIR /app

# Install curl (optional but useful for health checks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]