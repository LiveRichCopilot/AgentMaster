#!/bin/bash

# Monitor the deployment progress

echo "🔍 Monitoring agent deployments..."
echo ""

while true; do
  clear
  echo "╔═══════════════════════════════════════════════════════════╗"
  echo "║           VERTEX AI AGENT DEPLOYMENT MONITOR              ║"
  echo "╚═══════════════════════════════════════════════════════════╝"
  echo ""
  
  # Check deployed agents
  python3 /Users/liverichmedia/Agent\ master\ /genesis-agent/check_deployed_agents.py 2>/dev/null
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "RECENT LOG ACTIVITY:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  tail -20 /tmp/all_agents_deploy.log 2>/dev/null || echo "Deployment log not found"
  
  echo ""
  echo "Press Ctrl+C to stop monitoring | Refreshing in 30s..."
  sleep 30
done
