#!/bin/bash
# Start JAi Cortex OS - Complete Agent Development Kit

echo "🚀 Starting JAi Cortex OS - Complete Agent Development Kit"
echo "=" | awk '{for(i=0;i<70;i++) printf "="; print ""}'
echo ""

cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"

echo "🧠 Agent: JAi Cortex OS"
echo "🤖 Specialists: 24 deployed agents on Vertex AI"
echo "🛠️  Tools: Core tools + Specialist delegation"
echo "📡 Dev-UI: http://localhost:8000/dev-ui/?app=jai_cortex"
echo ""
echo "=" | awk '{for(i=0;i<70;i++) printf "="; print ""}'
echo ""

# Start ADK web interface
adk web --app jai_cortex --port 8000

