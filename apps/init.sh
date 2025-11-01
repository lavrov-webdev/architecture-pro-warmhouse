#!/bin/bash

# Exit on any error
set -e

echo "Starting the Smart Home Sensor API..."
echo "Building and starting containers..."
docker-compose up --build -d

echo "Waiting for services to be ready..."
# Wait for PostgreSQL to be ready
for i in {1..30}; do
  if docker exec smarthome-postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "PostgreSQL is ready!"
    break
  fi
  echo "Waiting for PostgreSQL to start... ($i/30)"
  sleep 1
done

# Check if PostgreSQL is ready
if ! docker exec smarthome-postgres pg_isready -U postgres > /dev/null 2>&1; then
  echo "Error: PostgreSQL did not start within the expected time."
  exit 1
fi

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/smart_home/init.sql"

# Run init SQL if database not present
echo "Checking database initialization state..."
if docker exec smarthome-postgres psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='smarthome'" | grep -q 1; then
  echo "Database 'smarthome' already exists. Applying schema changes..."
  if [ -f "$SQL_FILE" ]; then
    # Skip first 6 lines (CREATE DATABASE and \c) and apply to existing DB
    tail -n +7 "$SQL_FILE" | docker exec -i smarthome-postgres psql -U postgres -d smarthome -v ON_ERROR_STOP=1
    echo "Schema ensured."
  else
    echo "Warning: SQL file not found at $SQL_FILE; cannot apply schema."
  fi
else
  echo "Initializing database using init.sql..."
  if [ -f "$SQL_FILE" ]; then
    cat "$SQL_FILE" | docker exec -i smarthome-postgres psql -U postgres -v ON_ERROR_STOP=1
    echo "Database initialized."
  else
    echo "Warning: SQL file not found at $SQL_FILE; skipping database initialization."
  fi
fi

echo "All services are up and running!"
echo "The API is available at http://localhost:8080"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop the services, run: docker-compose down"