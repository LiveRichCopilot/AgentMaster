#!/bin/bash

# Deploy all agents quickly - submit and move on (don't wait for completion)

PROJECT="studio-2416451423-f2d96"
LOCATION="us-central1"

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

for AGENT in "${AGENTS[@]}"; do
  IFS=':' read -r DIR_NAME DISPLAY_NAME <<< "$AGENT"
  
  echo "🚀 Submitting: $DISPLAY_NAME"
  
  cd "/Users/liverichmedia/Agent master /genesis-agent/$DIR_NAME"
  
  # Run deployment in background with 5-minute timeout
  ( 
    timeout 300 bash -c "PYTHONPATH=. python3 app/agent_engine_app.py --project $PROJECT --location $LOCATION --agent-name $DISPLAY_NAME" > /tmp/${DISPLAY_NAME}_deploy.log 2>&1
  ) &
  
  # Small delay between submissions
  sleep 2
done

echo ""
echo "✅ All 21 deployments submitted!"
echo "⏳ They're building in the background (takes 5-10 min each)"
echo ""
echo "Check status with: python3 check_deployed_agents.py"
