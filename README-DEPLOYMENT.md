# ETERNITY CAPITAL CRM - Deployment Guide

## 🚀 One-Command Deployment

This project is now configured for **one-command deployment** for both development and production environments.

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **Node.js** (v16 or higher)
- **SSH access** to EC2 instance (for production deployment)

## 🔧 Quick Start

### Development (Local)

Start both frontend and backend locally with one command:

```bash
# Option 1: Using the script directly
./dev.sh

# Option 2: Using npm
npm run dev

# Option 3: Using npm start
npm start
```

This will:
- Start the Django backend with Docker Compose (PostgreSQL, Redis, Celery)
- Configure the frontend to proxy to local backend
- Start the Vue.js frontend development server
- Automatically wait for services to be ready

**Local URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/swagger/

### Production (EC2 Deployment)

Deploy both frontend and backend to EC2 with one command:

```bash
# Option 1: Using the script directly
./deploy.sh

# Option 2: Using npm
npm run deploy
```

This will:
- Build the Vue.js frontend for production
- Create production Docker Compose configuration
- Set up Nginx reverse proxy
- Transfer all files to EC2
- Deploy and start all services on EC2
- Run health checks

**Production URLs:**
- Frontend: http://13.210.124.119
- Backend API: http://13.210.124.119/api/
- Admin Panel: http://13.210.124.119/admin/
- API Documentation: http://13.210.124.119/api/swagger/

## 🛠️ Individual Commands

### Installation
```bash
# Install frontend dependencies
npm run install:frontend

# Install all dependencies
npm run install:all
```

### Backend Only
```bash
# Start backend services
npm run backend:start

# Stop backend services  
npm run backend:stop

# View backend logs
npm run backend:logs

# Check service status
npm run status
```

### Frontend Only
```bash
# Start frontend development server
npm run frontend:dev

# Build frontend for production
npm run build
```

## 🏗️ Architecture

### Development Setup
```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Vite Dev)    │◄──►│   (Docker)      │
│   :5173         │    │   :8000         │
└─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Services      │
                       │ PostgreSQL:5432 │
                       │ Redis:6379      │
                       │ Celery Workers  │
                       └─────────────────┘
```

### Production Setup
```
┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Backend       │
│   (Frontend)    │◄──►│   (Django)      │
│   :80           │    │   :8000         │
└─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Services      │
                       │ PostgreSQL:5432 │
                       │ Redis:6379      │
                       │ Celery Workers  │
                       └─────────────────┘
```

## 🔍 Health Checks

The deployment scripts include automatic health checks:

- **Backend**: Checks if Django API is responding
- **Frontend**: Verifies Nginx is serving the Vue.js app
- **Database**: Ensures PostgreSQL is ready
- **Cache**: Confirms Redis is operational

## 🔧 Configuration

### Environment Variables

The deployment automatically configures:

**Backend:**
- `DEBUG=0` (production) / `DEBUG=1` (development)
- Database credentials for PostgreSQL
- Redis connection for Celery
- Email SMTP settings for Gmail

**Frontend:**
- API proxy to correct backend URL
- Production build optimization
- Static asset handling

### Ports

**Development:**
- Frontend: 5173
- Backend: 8000
- PostgreSQL: 5433 (mapped to avoid conflicts)
- Redis: 6380

**Production:**
- Frontend: 80 (HTTP)
- Backend: 8000 (internal)
- PostgreSQL: 5432
- Redis: 6379

## 🚨 Troubleshooting

### Development Issues

1. **Docker not running:**
   ```bash
   # Start Docker Desktop first, then run:
   npm run dev
   ```

2. **Port conflicts:**
   ```bash
   # Stop existing services
   npm run backend:stop
   # Then restart
   npm run dev
   ```

3. **Frontend proxy errors:**
   - Check if backend is running: `npm run status`
   - Check backend logs: `npm run backend:logs`

### Production Issues

1. **SSH connection failed:**
   - Verify EC2 instance is running
   - Check SSH key permissions: `chmod 400 /Users/hongyuanfan/Desktop/mike.pem`

2. **Deployment failed:**
   - Check EC2 instance has enough resources
   - Verify Docker is installed on EC2
   - Check security group allows port 80

3. **Services not starting:**
   - SSH into EC2: `ssh -i /Users/hongyuanfan/Desktop/mike.pem ubuntu@13.210.124.119`
   - Check logs: `cd ~/backend && docker compose -f docker-compose.production.yml logs`

## 📊 Monitoring

### Check Service Status
```bash
# Local development
npm run status

# Production (SSH to EC2)
ssh -i /Users/hongyuanfan/Desktop/mike.pem ubuntu@13.210.124.119 "cd ~/backend && docker compose -f docker-compose.production.yml ps"
```

### View Logs
```bash
# Local development
npm run backend:logs

# Production (SSH to EC2)
ssh -i /Users/hongyuanfan/Desktop/mike.pem ubuntu@13.210.124.119 "cd ~/backend && docker compose -f docker-compose.production.yml logs -f"
```

## 🎯 Next Steps

1. **Custom Domain**: Point your domain to the EC2 IP address
2. **SSL Certificate**: Add HTTPS with Let's Encrypt
3. **Monitoring**: Set up application monitoring and alerts
4. **Backup**: Configure automated database backups
5. **CI/CD**: Set up automated deployments with GitHub Actions

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs using the provided commands
3. Verify all prerequisites are installed and configured 