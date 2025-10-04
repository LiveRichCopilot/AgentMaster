#!/bin/bash

# Start the TRUE AGENT backend
echo "🚀 Starting Agent Master TRUE AGENT..."

# Set environment variables
export GOOGLE_API_KEY="AIzaSyB4wJfH7CH6jL6h7QQZLUeCKzm6AEHkKVI"
export GOOGLE_GENAI_USE_VERTEXAI="False"
export PORT="8000"

# Navigate to backend directory
cd /Users/liverichmedia/Agent\ master\ /genesis-agent/agent_backend

# Start the server
echo "📡 Starting server on http://localhost:8000..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload


