#!/bin/bash
# Web Search API Setup Script

echo "=================================="
echo "🌐 Web Power-Up Configuration"
echo "=================================="
echo ""

# Check if .env.search exists
if [ ! -f ".env.search" ]; then
    echo "❌ Error: .env.search file not found!"
    echo "Please create it first with your API keys."
    exit 1
fi

# Source the environment file
source .env.search

# Check if keys are set
if [ "$GOOGLE_SEARCH_API_KEY" == "YOUR_API_KEY_HERE" ]; then
    echo "❌ Error: Please replace YOUR_API_KEY_HERE with your actual API key in .env.search"
    exit 1
fi

if [ "$GOOGLE_SEARCH_ENGINE_ID" == "YOUR_SEARCH_ENGINE_ID_HERE" ]; then
    echo "❌ Error: Please replace YOUR_SEARCH_ENGINE_ID_HERE with your actual Search Engine ID in .env.search"
    exit 1
fi

# Export the variables
export GOOGLE_SEARCH_API_KEY
export GOOGLE_SEARCH_ENGINE_ID
export SESSION_SERVICE_URI="sqlite:///./jai_cortex_sessions.db"

echo "✅ API Key configured: ${GOOGLE_SEARCH_API_KEY:0:10}..."
echo "✅ Search Engine ID configured: $GOOGLE_SEARCH_ENGINE_ID"
echo ""
echo "=================================="
echo "🚀 Starting JAi with Web Power-Up"
echo "=================================="
echo ""

# Kill existing server
pkill -f "adk web"
sleep 2

# Start server with all environment variables
# Note: Variables must be exported before running adk web
GOOGLE_SEARCH_API_KEY="$GOOGLE_SEARCH_API_KEY" \
GOOGLE_SEARCH_ENGINE_ID="$GOOGLE_SEARCH_ENGINE_ID" \
SESSION_SERVICE_URI="$SESSION_SERVICE_URI" \
adk web . > /tmp/adk_web_debug.log 2>&1 &

sleep 8

# Check if server started
if pgrep -f "adk web" > /dev/null; then
    echo "✅ Server started successfully with Web Power-Up!"
    echo ""
    echo "🌐 Access JAi at: http://localhost:8000/dev-ui/?app=jai_cortex"
    echo ""
    echo "🧪 Test queries:"
    echo "   • 'Research the latest AI agent developments'"
    echo "   • 'What are the pros and cons of React vs Vue in 2025?'"
    echo "   • 'Give me a comprehensive brief on quantum computing'"
    echo ""
    echo "⚡ Web Power-Up features:"
    echo "   • Searches 5 sources automatically"
    echo "   • Extracts full content from each"
    echo "   • Synthesizes findings with Gemini 2.5 Pro"
    echo "   • Provides citations for every claim"
    echo ""
else
    echo "❌ Server failed to start. Check /tmp/adk_web_debug.log for errors"
fi

