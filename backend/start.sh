#!/bin/bash
# Quick start script for LogiSuiEl-V4 backend

echo "==================================="
echo "LogiSuiEl-V4 Backend Setup"
echo "==================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo ""
echo "==================================="
echo "Starting FastAPI server..."
echo "==================================="
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""
echo "Default credentials:"
echo "  Admin: admin / admin"
echo "  Teacher: test / test"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
