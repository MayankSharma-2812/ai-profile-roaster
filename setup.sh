#!/bin/bash
# Setup script for production deployment

set -e

echo "🚀 AI Profile Roaster - Production Setup"
echo "========================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install production dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements-prod.txt
echo "✓ Dependencies installed"

# Download spaCy model
echo "🧠 Downloading spaCy model..."
python -m spacy download en_core_web_sm || echo "⚠️  spaCy model download optional"
echo "✓ spaCy model ready"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - GROQ_API_KEY (optional)"
    echo "   - SECRET_KEY (production mode)"
else
    echo "✓ .env file exists"
fi

# Test imports
echo "🧪 Testing imports..."
python -c "from web.app import app; print('✓ App imports successfully')"

# Show next steps
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run development server: python -m web.app"
echo "3. Or run with gunicorn: gunicorn -b 0.0.0.0:8500 web.app:app"
echo ""
echo "For Docker deployment:"
echo "  docker-compose up --build"
echo ""
