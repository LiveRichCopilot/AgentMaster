#!/bin/bash
# Fix pywin32 issue in all agent directories

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

echo "🔧 Removing pywin32 from all agent requirements..."
echo ""

for agent in "${AGENTS[@]}"; do
  if [ -d "$agent" ]; then
    if [ -f "$agent/.requirements.txt" ]; then
      if grep -q "pywin32" "$agent/.requirements.txt"; then
        echo "  🧹 Fixing: $agent"
        grep -v "pywin32" "$agent/.requirements.txt" > "$agent/.requirements.txt.new"
        mv "$agent/.requirements.txt.new" "$agent/.requirements.txt"
      else
        echo "  ✅ Clean: $agent"
      fi
    else
      echo "  ⚠️  No requirements: $agent"
    fi
  fi
done

echo ""
echo "✅ All agents fixed!"
