#!/bin/zsh
# Quick Start Script for Phishing URL Scanner
# This script runs the entire project setup and training in one go

set -e

PROJECT_DIR="/Users/ziauddin/Phishing URL Scanner"
cd "$PROJECT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                  PHISHING URL SCANNER - QUICK START                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Virtual Environment
echo "📦 Step 1: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Step 2: Activate and Install
echo "📥 Step 2: Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Step 3: Train Models
echo "🤖 Step 3: Training ML models (Random Forest + SVM)..."
python train_models.py
echo ""

# Step 4: Success message
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ SETUP COMPLETE!                                      ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Your models are trained and ready!"
echo ""
echo "🚀 NEXT: Start the API server"
echo "   Run this command in this terminal:"
echo ""
echo "   python src/app.py"
echo ""
echo "📡 THEN: Test the API"
echo "   Open a NEW terminal and run:"
echo ""
echo "   cd \"Phishing URL Scanner\""
echo "   source venv/bin/activate"
echo "   python test_api.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 For all commands, see: COMMANDS.txt"
echo "📖 For detailed guide, see: GETTING_STARTED.md"
echo ""
