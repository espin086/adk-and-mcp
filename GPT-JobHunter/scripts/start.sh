#!/bin/bash

# GPT-JobHunter Quick Start Script

set -e

echo "🚀 Starting GPT-JobHunter..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before proceeding."
    echo "   Especially set your OPENAI_API_KEY for AI features to work."
    read -p "Press enter to continue..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads logs

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Health check
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Check frontend
if curl -f http://localhost:8501 &> /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend health check failed"
fi

echo ""
echo "🎉 GPT-JobHunter is now running!"
echo ""
echo "📱 Access the application:"
echo "   Frontend:        http://localhost:8501"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   API ReDoc:       http://localhost:8000/redoc"
echo ""
echo "🛑 To stop the application, run: docker-compose down"
echo "🔄 To restart the application, run: docker-compose restart"
echo "📊 To view logs, run: docker-compose logs -f"