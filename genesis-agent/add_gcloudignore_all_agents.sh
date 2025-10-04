#!/bin/bash
# Add .gcloudignore to all agent directories to exclude .venv

AGENTS=(
  "codemaster-agent"
  "databaseexpert-agent"
  "backupmanager-agent"
  "financewizard-agent"
  "researchscout-agent"
  "designgenius-agent"
  "apiexpert-agent"
  "workspacemanager-agent"
  "mediaprocessor-agent"
  "agentcreator-agent"
  "cryptoking-agent"
  "stockmaster-agent"
  "travelgenius-agent"
  "shopsavvy-agent"
  "budgetboss-agent"
  "mindreader-agent"
  "sportsmath-agent"
  "automationwizard-agent"
  "notebookgenius-agent"
  "cloudmaster-agent"
  "docsgenius-agent"
  "integrationpro-agent"
  "metricsmonitor-agent"
  "visionmaster-agent"
  "competitorwatch-agent"
  "mapsnavigator-agent"
  "securityguard-agent"
)

IGNORE_CONTENT="# Exclude virtual environment
.venv/
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
*.log
.env
.git/"

echo "📝 Adding .gcloudignore to all agent directories..."
echo ""

for agent in "${AGENTS[@]}"; do
  if [ -d "$agent" ]; then
    echo "$IGNORE_CONTENT" > "$agent/.gcloudignore"
    echo "  ✅ Created: $agent/.gcloudignore"
  fi
done

echo ""
echo "✅ All agents updated!"
