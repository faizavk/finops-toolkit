#!/bin/bash

# Start Frontend Server
echo "Starting FinOps Toolkit Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the React development server
echo "Starting React app on http://localhost:3000"
npm start

