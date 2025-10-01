#!/bin/bash

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for database to be ready
wait_for_database() {
    print_status "Waiting for database to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker exec postgres pg_isready -U postgres -d postgres >/dev/null 2>&1; then
            print_success "Database is ready!"
            return 0
        fi
        print_status "Attempt $attempt/$max_attempts - Database not ready yet, waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Database failed to start within expected time"
    exit 1
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    make database-down
}
trap cleanup EXIT

print_status "Starting Earthquake API setup..."

# Check required tools
print_status "Checking required tools..."

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.12 or later."
    exit 1
fi

if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "All required tools are available"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
API_USERNAME=admin
API_PASSWORD=admin
API_REALM=EarthquakeAPI
EOF
    print_success ".env file created with default values"
else
    print_status ".env file already exists"
fi

# Check if virtual environment exists, create if not
if [ ! -d .venv ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Install Poetry inside the virtual environment
print_status "Installing Poetry in virtual environment..."
pip install poetry

# Install dependencies with Poetry
if [ ! -f poetry.lock ]; then
    print_status "Installing dependencies with Poetry..."
    poetry install --with optional
    print_success "Dependencies installed"
else
    print_status "Updating dependencies with Poetry..."
    poetry install --with optional
    print_success "Dependencies updated"
fi

# Start the database
print_status "Starting database..."
make database-up

# Wait for database to be ready
wait_for_database

# Run migrations
print_status "Running database migrations..."
make migrate
print_success "Migrations completed"

# Start the API
print_status "Starting FastAPI server..."
print_success "Setup complete! API will be available at http://localhost:8000"
print_status "Press Ctrl+C to stop the server and cleanup"

poetry run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000