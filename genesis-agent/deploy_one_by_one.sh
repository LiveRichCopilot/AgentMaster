#!/bin/bash

# Deploy agents ONE AT A TIME - the method that actually works

BASE_DIR="/Users/liverichmedia/Agent master /genesis-agent"

# List of agents (skip file-manager since it's already deployed)
AGENTS=(
    "codemaster:CodeMaster"
    "dataprocessor:DataProcessor"
    "notekeeper:NoteKeeper"
    "mediaprocessor:MediaProcessor"
    "databaseexpert:DatabaseExpert"
    "apiintegrator:APIIntegrator"
    "websearcher:WebSearcher"
    "cloudexpert:CloudExpert"
    "automationwizard:AutomationWizard"
    "securityguard:SecurityGuard"
    "backupmanager:BackupManager"
    "notebookscientist:NotebookScientist"
    "documentparser:DocumentParser"
    "visionanalyzer:VisionAnalyzer"
    "emailmanager:EmailManager"
    "calendarmanager:CalendarManager"
    "personalassistant:PersonalAssistant"
    "knowledgebase:KnowledgeBase"
    "workspacemanager:WorkspaceManager"
    "performancemonitor:PerformanceMonitor"
    "errorhandler:ErrorHandler"
    "versioncontroller:VersionController"
    "metaagent:MetaAgent"
)

DEPLOYED=0
FAILED=0

echo "🚀 DEPLOYING 23 AGENTS ONE AT A TIME"
echo "========================================"
echo ""

for agent in "${AGENTS[@]}"; do
    IFS=':' read -r DIR_NAME AGENT_NAME <<< "$agent"
    AGENT_DIR="$BASE_DIR/${DIR_NAME}-agent"
    
    echo "📦 [$((DEPLOYED + FAILED + 1))/23] Deploying: $AGENT_NAME"
    
    cd "$AGENT_DIR"
    
    # Run deployment
    uv run app/agent_engine_app.py --agent-name "$AGENT_NAME" > /tmp/${AGENT_NAME}_deploy.log 2>&1
    
    # Check if successful
    if grep -q "Deployment successful" /tmp/${AGENT_NAME}_deploy.log; then
        echo "✅ $AGENT_NAME deployed!"
        ((DEPLOYED++))
    else
        echo "❌ $AGENT_NAME failed"
        echo "   Error: $(tail -5 /tmp/${AGENT_NAME}_deploy.log | head -1)"
        ((FAILED++))
    fi
    
    echo ""
    
    # Show progress
    echo "   Progress: $DEPLOYED deployed, $FAILED failed"
    echo ""
done

echo "========================================"
echo "✅ Successfully deployed: $DEPLOYED agents"
echo "❌ Failed: $FAILED agents"
echo ""
echo "🌐 https://console.cloud.google.com/vertex-ai/reasoning-engines?project=studio-2416451423-f2d96"

