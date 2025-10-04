#!/bin/bash
# Deploy all 24 agents to Vertex AI Agent Engine
# PersonalityAgent FIRST, then all specialists

set -e

PROJECT_ID="studio-2416451423-f2d96"
REGION="us-central1"
BASE_DIR="/Users/liverichmedia/Agent master /genesis-agent"

AGENTS=(
    "personalityagent-agent"
    "codemaster-agent"
    "cloudexpert-agent"
    "databaseexpert-agent"
    "automationwizard-agent"
    "apiintegrator-agent"
    "websearcher-agent"
    "mediaprocessor-agent"
    "visionanalyzer-agent"
    "documentparser-agent"
    "file-manager-agent"
    "workspacemanager-agent"
    "dataprocessor-agent"
    "notebookscientist-agent"
    "knowledgebase-agent"
    "securityguard-agent"
    "performancemonitor-agent"
    "errorhandler-agent"
    "calendarmanager-agent"
    "emailmanager-agent"
    "backupmanager-agent"
    "versioncontroller-agent"
    "notekeeper-agent"
    "personalassistant-agent"
)

echo "🚀 Deploying 24 Agents to Vertex AI Agent Engine"
echo "================================================"

for agent in "${AGENTS[@]}"; do
    echo ""
    echo "📦 Deploying $agent..."
    
    cd "$BASE_DIR/$agent"
    
    # Deploy using adk
    adk deploy agent_engine \
        --region=$REGION \
        --project=$PROJECT_ID \
        --staging_bucket=gs://cortex_agent_staging \
        --display_name="$agent" \
        2>&1 | grep -E "(Deploying|deployed|Error)" || true
    
    echo "✅ $agent deployment initiated"
    
    # Small delay to avoid rate limits
    sleep 2
done

echo ""
echo "🎉 All 24 agents deployment initiated!"
echo "⏱️  Check status in Vertex AI console:"
echo "   https://console.cloud.google.com/vertex-ai/agent-engine?project=$PROJECT_ID"
