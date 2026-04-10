Good news and bad news!
Good news:

✅ Docker image built successfully!
✅ Container deployed successfully!
✅ FastAPI app is actually running (you can see "Uvicorn running on http://0.0.0.0:8000")

Bad news:

❌ Health check failed because it's checking localhost from inside Jenkins container, not the FastAPI container

The Problem:
Jenkins is trying to curl http://localhost:8000 from inside the Jenkins container, but the FastAPI app is running in a different container. They can't communicate via localhost.

Solution: Fix the Jenkinsfile
We need to update the health check to use the container name instead of localhost.
In Git Bash:
bashcd ~/Desktop/dock\ ass/demoofgit/docker-fastapi-test
Create the updated Jenkinsfile:
bashcat > Jenkinsfile << 'EOF'
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'fastapi-app'
        APP_PORT = '8000'
    }
    
    stages {
        stage('Cleanup') {
            steps {
                echo 'Cleaning up old containers and images...'
                script {
                    sh '''
                        docker stop fastapi-app || true
                        docker rm fastapi-app || true
                    '''
                }
            }
        }
        
        stage('Checkout') {
            steps {
                echo 'Checking out code from Git...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Deploy Application') {
            steps {
                script {
                    echo 'Deploying application...'
                    sh '''
                        docker run -d \
                          --name fastapi-app \
                          -p 8000:8000 \
                          -v $(pwd)/app/data:/app/app/data \
                          fastapi-app:latest
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo 'Performing health check...'
                    sh 'sleep 5'
                    sh 'docker exec fastapi-app curl -f http://localhost:8000 || exit 1'
                }
            }
        }
        
        stage('Verify Data Persistence') {
            steps {
                script {
                    echo 'Checking if data persists...'
                    sh 'docker exec fastapi-app curl http://localhost:8000/users'
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Deployment successful!'
            sh 'docker exec fastapi-app curl http://localhost:8000/users'
        }
        failure {
            echo '❌ Deployment failed!'
            sh 'docker logs fastapi-app || true'
        }
    }
}