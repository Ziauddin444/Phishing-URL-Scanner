#!/bin/bash

# Phishing URL Scanner - Setup Script
# This script sets up the complete development environment

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  PHISHING URL SCANNER - SETUP & QUICK START GUIDE              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo -e "\n${BLUE}[1/6]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3.7 or higher from https://www.python.org"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Step 2: Create virtual environment
echo -e "\n${BLUE}[2/6]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Step 3: Activate virtual environment
echo -e "\n${BLUE}[3/6]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Step 4: Install dependencies
echo -e "\n${BLUE}[4/6]${NC} Installing Python dependencies..."
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Step 5: Create necessary directories
echo -e "\n${BLUE}[5/6]${NC} Setting up project directories..."
mkdir -p models data logs
touch .env
echo -e "${GREEN}✅ Directories created${NC}"

# Step 6: Display next steps
echo -e "\n${BLUE}[6/6]${NC} Setup complete!"

echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  SETUP COMPLETE - NEXT STEPS                                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${YELLOW}Step 1: Train the ML Models${NC}"
echo "   Run: python train_models.py"
echo "   This trains Random Forest and SVM models (takes 1-2 minutes)"

echo -e "\n${YELLOW}Step 2: Start the Flask API${NC}"
echo "   Run: python src/app.py"
echo "   API will be available at: http://localhost:5000"

echo -e "\n${YELLOW}Step 3: Test the API (in another terminal)${NC}"
echo "   Run: python test_api.py"

echo -e "\n${YELLOW}Step 4: Make Predictions${NC}"
echo "   POST http://localhost:5000/api/predict"
echo "   Body: {\"url\": \"https://example.com\"}"

echo -e "\n${BLUE}📚 Documentation Files:${NC}"
echo "   • README.md - Complete project documentation"
echo "   • API_DOCUMENTATION.md - API reference guide"
echo "   • example_heuristic_analysis.py - Feature analysis example"

echo -e "\n${BLUE}📂 Project Structure:${NC}"
echo "   src/app.py - Flask REST API"
echo "   src/predictor.py - ML prediction engine"
echo "   src/model_trainer.py - Model training code"
echo "   src/heuristic_analyzer.py - URL feature extraction"
echo "   models/ - Trained ML models (after training)"

echo -e "\n${BLUE}🚀 Quick Commands:${NC}"
echo "   • Train models: python train_models.py"
echo "   • Run API: python src/app.py"
echo "   • Test API: python test_api.py"
echo "   • Example: python example_heuristic_analysis.py"

echo -e "\n${GREEN}Happy coding! 🔒${NC}\n"
