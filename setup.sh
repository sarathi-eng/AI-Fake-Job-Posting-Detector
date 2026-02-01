#!/usr/bin/env bash
# Quick start script for the Fake Job Posting Detector

set -e

echo "🚀 Fake Job Posting Detector - Setup"
echo "===================================="

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run tests:        source venv/bin/activate && python test_detector.py"
echo "2. Start API:        source venv/bin/activate && python -m uvicorn api.main:app --reload"
echo "3. Test API:         source venv/bin/activate && python test_api.py"
echo "4. View API docs:    http://localhost:8000/docs"
echo ""
