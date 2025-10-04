#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              STARTING JAI CORTEX SYSTEM                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if agent registry exists
if [ ! -f "agent_registry.json" ]; then
    echo "⚠️  Agent registry not found. Running wire_agents.py..."
    python3 wire_agents.py
fi

echo "🚀 Starting MetaAgent API Backend (port 8080)..."
cd agent_backend
python3 -m uvicorn metaagent_api:app --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!
echo "  Backend PID: $BACKEND_PID"

sleep 3

echo ""
echo "🎨 Starting Chat UI Frontend (port 3000)..."
cd ../cortex-chat-ui
npm run dev &
FRONTEND_PID=$!
echo "  Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ JAI CORTEX IS RUNNING!"
echo ""
echo "📍 Access points:"
echo "  • Chat UI:      http://localhost:3000"
echo "  • MetaAgent API: http://localhost:8080"
echo "  • API Docs:      http://localhost:8080/docs"
echo ""
echo "🤖 Connected Agents: 26 (24 specialists + MetaAgent + routing)"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
wait
