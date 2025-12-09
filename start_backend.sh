#!/bin/bash

# Start Backend Server
echo "Starting FinOps Toolkit Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the Flask server
echo "Starting Flask server on http://localhost:5000"
python app.py

