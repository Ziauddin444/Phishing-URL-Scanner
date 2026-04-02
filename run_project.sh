#!/bin/zsh
# Complete project run script for Phishing URL Scanner

set -e  # Exit on error

PROJECT_DIR="/Users/ziauddin/Phishing URL Scanner"
cd "$PROJECT_DIR"

echo "================================================================================"
echo "PHISHING URL SCANNER - COMPLETE PROJECT RUN"
echo "================================================================================"
echo ""

# Step 1: Create virtual environment if it doesn't exist
echo "STEP 1: Setting up virtual environment..."
echo "================================================================================"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Step 2: Activate virtual environment and install dependencies
echo "STEP 2: Installing dependencies..."
echo "================================================================================"
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 3: Train the models
echo "STEP 3: Training ML models..."
echo "================================================================================"
python train_models.py
echo ""

# Step 4: Print next steps
echo "================================================================================"
echo "TRAINING COMPLETED!"
echo "================================================================================"
echo ""
echo "Next steps to run the API:"
echo "1. Start the API server:"
echo "   python src/app.py"
echo ""
echo "2. In another terminal, test the API:"
echo "   python test_api.py"
echo ""
echo "Or use curl commands to test specific endpoints:"
echo "   curl http://localhost:5000/api/health"
echo "   curl -X POST http://localhost:5000/api/predict -H 'Content-Type: application/json' -d '{\"url\": \"https://google.com\"}'"
echo ""
