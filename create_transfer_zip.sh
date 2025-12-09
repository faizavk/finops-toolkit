#!/bin/bash
# Script to create a clean ZIP file for Windows transfer

echo "=========================================="
echo "  Creating Transfer ZIP for Windows"
echo "=========================================="
echo ""

# Navigate to Desktop
cd /Users/summaiya.sarvari/Desktop

# Remove old ZIP if exists
if [ -f "finops-project.zip" ]; then
    echo "Removing old ZIP file..."
    rm finops-project.zip
fi

echo "Creating ZIP file (excluding venv, node_modules, etc.)..."
zip -r finops-project.zip fin \
  -x "*.DS_Store" \
  -x "*/venv/*" \
  -x "*/node_modules/*" \
  -x "*/__pycache__/*" \
  -x "*/logs/*" \
  -x "*/.env" \
  -x "*/build/*" \
  -x "*.pyc" \
  -x "*/.git/*" \
  -x "*/\.*" \
  -x "*/node_modules/**/*"

echo ""
echo "=========================================="
echo "  ZIP Created Successfully!"
echo "=========================================="
echo ""
echo "File: finops-project.zip"
echo "Location: /Users/summaiya.sarvari/Desktop/"
echo ""
ls -lh finops-project.zip
echo ""
echo "Next steps:"
echo "1. Transfer ZIP to Windows machine"
echo "2. Extract ZIP on Windows"
echo "3. Follow CROSS_PLATFORM_MIGRATION.md"
echo ""
