#!/bin/bash

# Development Setup Script
# This script starts both frontend and backend for local development

set -e

echo "🚀 Starting development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "🧹 Cleaning up..."
    kill $(jobs -p) 2>/dev/null || true
    exit
}

# Set cleanup trap
trap cleanup EXIT INT TERM

BACKEND_DIR="PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891"
FRONTEND_DIR="ICfding/ICprivate-funding"

# Start backend services
echo "🐳 Starting backend services..."
cd "$BACKEND_DIR"
docker-compose up -d
cd - > /dev/null

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
timeout 60 bash -c 'until curl -f http://localhost:8000/api/swagger/ > /dev/null 2>&1; do sleep 2; done' || {
    echo "❌ Backend failed to start within 60 seconds"
    exit 1
}

echo "✅ Backend is ready at http://localhost:8000"

# Update frontend config for local development
echo "📝 Configuring frontend for local development..."
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
        target: "http://localhost:8000", 
        changeOrigin: true,
        secure: false,
      },
    },
    cors: true,
  },
});
EOF

# Start frontend
echo "🌐 Starting frontend..."
cd "$FRONTEND_DIR"
npm install
npm run dev &
FRONTEND_PID=$!
cd - > /dev/null

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000/api/"
echo "   Admin Panel: http://localhost:8000/admin/"
echo "   API Documentation: http://localhost:8000/api/swagger/"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for frontend process
wait $FRONTEND_PID 