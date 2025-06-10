#!/bin/bash

# Unified Frontend and Backend Deployment Script
# This script deploys both the frontend and backend to the EC2 instance

set -e  # Exit on any error

# Configuration
EC2_IP="13.210.124.119"
SSH_KEY="/Users/hongyuanfan/Desktop/mike.pem"
BACKEND_DIR="PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891"
FRONTEND_DIR="ICfding/ICprivate-funding"

echo "🚀 Starting unified deployment process..."

# Step 1: Update frontend configuration for production
echo "📝 Updating frontend configuration..."
cat > "$FRONTEND_DIR/vite.config.js" << 'EOF'
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://13.210.124.119:8000", 
        changeOrigin: true,
        secure: false,
      },
    },
    cors: true,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
});
EOF

# Step 2: Build frontend
echo "🏗️  Building frontend..."
cd "$FRONTEND_DIR"
npm install
npm run build
cd - > /dev/null

# Step 3: Create unified Docker Compose configuration
echo "🐳 Creating unified Docker Compose configuration..."
cat > "$BACKEND_DIR/docker-compose.production.yml" << 'EOF'
services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=crm_loan_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backenddjango
    command: >
      sh -c "python manage.py wait_for_db &&
             python manage.py collectstatic --noinput &&
             python manage.py migrate &&
             gunicorn crm_backend.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - ./backenddjango:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DEBUG=0
      - POSTGRES_DB=crm_loan_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
      - PYTHONUNBUFFERED=1
      - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
      - EMAIL_HOST=smtp.gmail.com
      - EMAIL_PORT=587
      - EMAIL_USE_TLS=True
      - EMAIL_HOST_USER=fanhongyuan897@gmail.com
      - EMAIL_HOST_PASSWORD=oytebasqthbbjvdd
      - DEFAULT_FROM_EMAIL=fanhongyuan897@gmail.com

  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend

  celery:
    build: ./backenddjango
    command: >
      sh -c "python manage.py wait_for_db &&
             celery -A crm_backend worker -l info"
    volumes:
      - ./backenddjango:/app
    depends_on:
      - backend
      - redis
    environment:
      - DEBUG=0
      - POSTGRES_DB=crm_loan_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
      - PYTHONUNBUFFERED=1

  celery-beat:
    build: ./backenddjango
    command: >
      sh -c "python manage.py wait_for_db &&
             celery -A crm_backend beat -l info"
    volumes:
      - ./backenddjango:/app
    depends_on:
      - backend
      - redis
    environment:
      - DEBUG=0
      - POSTGRES_DB=crm_loan_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
      - PYTHONUNBUFFERED=1

volumes:
  postgres_data:
  static_volume:
  media_volume:
EOF

# Step 4: Create Nginx configuration
echo "🌐 Creating Nginx configuration..."
cat > "$BACKEND_DIR/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name _;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Django Admin
        location /admin/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            proxy_pass http://backend:8000;
        }

        # Media files
        location /media/ {
            proxy_pass http://backend:8000;
        }
    }
}
EOF

# Step 5: Transfer everything to EC2
echo "📡 Transferring files to EC2..."
# Create directories on EC2 first
ssh -i "$SSH_KEY" ubuntu@$EC2_IP "mkdir -p ~/backend/frontend/dist"

rsync -avz --progress --delete -e "ssh -i $SSH_KEY" "$BACKEND_DIR/" ubuntu@$EC2_IP:~/backend/
rsync -avz --progress -e "ssh -i $SSH_KEY" "$FRONTEND_DIR/dist/" ubuntu@$EC2_IP:~/backend/frontend/dist/

# Step 6: Deploy on EC2
echo "🚀 Deploying on EC2..."
ssh -i "$SSH_KEY" ubuntu@$EC2_IP << 'ENDSSH'
cd ~/backend

# Stop any existing containers
docker compose -f docker-compose.production.yml down || true

# Build and start services
docker compose -f docker-compose.production.yml build
docker compose -f docker-compose.production.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service status
echo "📊 Service Status:"
docker compose -f docker-compose.production.yml ps

# Check backend health
echo "🏥 Checking backend health..."
curl -f http://localhost:8000/api/swagger/ > /dev/null 2>&1 && echo "✅ Backend is healthy" || echo "❌ Backend health check failed"

# Check frontend
echo "🖥️  Checking frontend..."
curl -f http://localhost/ > /dev/null 2>&1 && echo "✅ Frontend is serving" || echo "❌ Frontend check failed"

echo "🎉 Deployment complete!"
echo "🌐 Frontend: http://13.210.124.119"
echo "🔧 Backend API: http://13.210.124.119/api/"
echo "⚙️  Admin Panel: http://13.210.124.119/admin/"
ENDSSH

echo "✅ Unified deployment completed successfully!"
echo ""
echo "🌍 Your application is now live at:"
echo "   Frontend: http://13.210.124.119"
echo "   Backend API: http://13.210.124.119/api/"
echo "   Admin Panel: http://13.210.124.119/admin/"
echo "   API Documentation: http://13.210.124.119/api/swagger/" 