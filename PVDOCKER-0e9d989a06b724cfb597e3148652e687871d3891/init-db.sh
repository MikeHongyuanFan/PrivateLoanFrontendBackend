#!/bin/bash
set -e

# Start PostgreSQL container
docker-compose up -d db

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
sleep 10

# Create admin user
echo "Creating admin user in PostgreSQL..."
docker exec -it pvdocker-0e9d989a06b724cfb597e3148652e687871d3891-db-1 psql -U postgres -c "CREATE USER admin WITH PASSWORD 'admin' CREATEDB;"

# Stop the container
docker-compose down

# Start all services
echo "Starting all services..."
docker-compose up -d
