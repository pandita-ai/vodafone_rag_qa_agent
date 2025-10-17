#!/bin/bash

# Paralegal RAG Agent Startup Script

echo "🚀 Starting Paralegal AI Assistant..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "   OPENAI_API_KEY=your_openai_api_key_here"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker compose build

echo "🚀 Starting services..."
docker compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if the service is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Paralegal AI Assistant is running!"
    echo ""
    echo "🌐 Web Interface: http://localhost:8000/demo"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "❤️  Health Check: http://localhost:8000/health"
    echo ""
    echo "🛑 To stop the service: docker compose down"
else
    echo "❌ Service failed to start. Check logs with: docker compose logs"
fi
