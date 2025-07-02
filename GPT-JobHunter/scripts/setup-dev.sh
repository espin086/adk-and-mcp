#!/bin/bash

# GPT-JobHunter Development Setup Script

set -e

echo "🛠️  Setting up GPT-JobHunter for local development..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version: $PYTHON_VERSION"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration."
fi

# Setup backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment for backend..."
    python3 -m venv venv
fi

echo "📦 Installing backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment for frontend..."
    python3 -m venv venv
fi

echo "📦 Installing frontend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads logs

# Create start scripts
echo "📝 Creating convenience scripts..."

# Backend start script
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x start-backend.sh

# Frontend start script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
source venv/bin/activate
export API_BASE_URL=http://localhost:8000
streamlit run app.py
EOF
chmod +x start-frontend.sh

echo ""
echo "✅ Development setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Start backend:  ./start-backend.sh"
echo "   2. Start frontend: ./start-frontend.sh"
echo ""
echo "📱 Access the application:"
echo "   Frontend:        http://localhost:8501"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo ""
echo "💡 Note: You'll need to set up PostgreSQL and Redis manually for full functionality."
echo "   Or use Docker Compose: docker-compose up postgres redis"