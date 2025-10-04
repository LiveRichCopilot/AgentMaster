#!/bin/bash
# Start JAi Cortex OS with persistent sessions

cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"

# Set session persistence
export SESSION_SERVICE_URI="sqlite:///./jai_cortex_sessions.db"

# Start ADK web server
exec adk web --port 8000 --reload

