#!/bin/zsh

echo "🚀 Starting CORTEX OS with Vertex AI..."

# Kill any existing server
pkill -9 -f "uvicorn main:app" 2>/dev/null
sleep 2

# Navigate to backend directory
cd /Users/liverichmedia/Agent\ master\ /genesis-agent/agent_backend

# Set Vertex AI environment variables (CRITICAL - must be set BEFORE Python starts)
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96
export GOOGLE_CLOUD_LOCATION=us-central1

# Unset API key if it exists (Vertex AI should be used instead)
unset GOOGLE_API_KEY
unset GOOGLE_GENAI_API_KEY

echo "✅ Environment configured for Vertex AI"
echo "📍 Project: $GOOGLE_CLOUD_PROJECT"
echo "📍 Location: $GOOGLE_CLOUD_LOCATION"
echo "📍 Vertex AI: $GOOGLE_GENAI_USE_VERTEXAI"
echo ""
echo "🔄 Starting server..."
echo ""

# Start server with uvicorn
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload


