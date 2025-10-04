#!/bin/bash

# Deploy all agents using the custom agent_engine_app.py script
# This is the WORKING method that deployed BackupManager successfully

PROJECT="studio-2416451423-f2d96"
LOCATION="us-central1"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   🤖 DEPLOYING ALL AGENTS TO VERTEX AI 🤖                 ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# List of agents to deploy (skip ones that are already deployed)
AGENTS=(
  "apiintegrator-agent:ApiIntegrator"
  "automationwizard-agent:AutomationWizard"
  "calendarmanager-agent:CalendarManager"
  "cloudexpert-agent:CloudExpert"
  "databaseexpert-agent:DatabaseExpert"
  "dataprocessor-agent:DataProcessor"
  "documentparser-agent:DocumentParser"
  "emailmanager-agent:EmailManager"
  "errorhandler-agent:ErrorHandler"
  "knowledgebase-agent:KnowledgeBase"
  "mediaprocessor-agent:MediaProcessor"
  "metaagent-agent:MetaAgent"
  "notebookscientist-agent:NotebookScientist"
  "notekeeper-agent:NoteKeeper"
  "performancemonitor-agent:PerformanceMonitor"
  "personalassistant-agent:PersonalAssistant"
  "securityguard-agent:SecurityGuard"
  "versioncontroller-agent:VersionController"
  "visionanalyzer-agent:VisionAnalyzer"
  "websearcher-agent:WebSearcher"
  "workspacemanager-agent:WorkspaceManager"
)

SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_AGENTS=()

for AGENT in "${AGENTS[@]}"; do
  IFS=':' read -r DIR_NAME DISPLAY_NAME <<< "$AGENT"
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Deploying: $DISPLAY_NAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  cd "/Users/liverichmedia/Agent master /genesis-agent/$DIR_NAME" || {
    echo "❌ Directory not found: $DIR_NAME"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAILED_AGENTS+=("$DISPLAY_NAME (dir not found)")
    continue
  }
  
  if [ ! -f "app/agent_engine_app.py" ]; then
    echo "❌ No agent_engine_app.py found in $DIR_NAME"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAILED_AGENTS+=("$DISPLAY_NAME (no deploy script)")
    continue
  fi
  
  # Deploy using PYTHONPATH
  if PYTHONPATH=. python3 app/agent_engine_app.py \
    --project "$PROJECT" \
    --location "$LOCATION" \
    --agent-name "$DISPLAY_NAME" 2>&1 | tee "/tmp/${DISPLAY_NAME}_deploy.log"; then
    
    echo "✅ $DISPLAY_NAME deployed successfully!"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  else
    echo "❌ $DISPLAY_NAME deployment failed!"
    echo "   Check logs: /tmp/${DISPLAY_NAME}_deploy.log"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAILED_AGENTS+=("$DISPLAY_NAME")
  fi
  
  # Small delay between deployments
  sleep 5
done

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                 DEPLOYMENT SUMMARY                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Successful: $SUCCESS_COUNT"
echo "❌ Failed: $FAIL_COUNT"

if [ ${#FAILED_AGENTS[@]} -gt 0 ]; then
  echo ""
  echo "Failed agents:"
  for AGENT in "${FAILED_AGENTS[@]}"; do
    echo "  - $AGENT"
  done
fi

echo ""
echo "🌐 View all agents:"
echo "https://console.cloud.google.com/vertex-ai/reasoning-engines?project=$PROJECT"
