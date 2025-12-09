@echo off
REM Windows Batch Script to Start Frontend Server
REM Usage: Double-click this file or run from command prompt

echo ========================================
echo   FinOps Toolkit - Frontend Server
echo ========================================
echo.

cd /d %~dp0frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Node modules not found. Installing...
    echo This may take a few minutes...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Make sure Node.js is installed and in PATH
        pause
        exit /b 1
    )
)

echo.
echo Starting React development server...
echo Frontend will run on: http://localhost:3000
echo Browser should open automatically
echo Press Ctrl+C to stop the server
echo.

npm start

pause

