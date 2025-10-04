#!/bin/bash
# Deploy all 24 agents to Vertex AI Agent Engine (one at a time, pywin32 fixed)

PROJECT="studio-2416451423-f2d96"
LOCATION="us-central1"
BUCKET="cortex_agent_staging"

# All agent directories (in order)
AGENTS=(
  "codemaster-agent:CodeMaster"
  "databaseexpert-agent:DatabaseExpert"
  "backupmanager-agent:BackupManager"
  "financewizard-agent:FinanceWizard"
  "researchscout-agent:ResearchScout"
  "designgenius-agent:DesignGenius"
  "apiexpert-agent:APIExpert"
  "workspacemanager-agent:WorkspaceManager"
  "mediaprocessor-agent:MediaProcessor"
  "agentcreator-agent:AgentCreator"
  "cryptoking-agent:CryptoKing"
  "stockmaster-agent:StockMaster"
  "travelgenius-agent:TravelGenius"
  "shopsavvy-agent:ShopSavvy"
  "budgetboss-agent:BudgetBoss"
  "mindreader-agent:MindReader"
  "sportsmath-agent:SportsMath"
  "automationwizard-agent:AutomationWizard"
  "notebookgenius-agent:NotebookGenius"
  "cloudmaster-agent:CloudMaster"
  "docsgenius-agent:DocsGenius"
  "integrationpro-agent:IntegrationPro"
  "metricsmonitor-agent:MetricsMonitor"
  "visionmaster-agent:VisionMaster"
  "competitorwatch-agent:CompetitorWatch"
  "mapsnavigator-agent:MapsNavigator"
  "securityguard-agent:SecurityGuard"
)

TOTAL=${#AGENTS[@]}
SUCCESS=0
FAILED=0

echo "🚀 Deploying $TOTAL agents to Vertex AI Agent Engine"
echo "📍 Project: $PROJECT"
echo "📍 Location: $LOCATION"
echo "=================================================="
echo ""

for i in "${!AGENTS[@]}"; do
  IFS=':' read -r DIR NAME <<< "${AGENTS[$i]}"
  NUM=$((i + 1))
  
  echo "📦 [$NUM/$TOTAL] Deploying: $NAME"
  echo "   Directory: $DIR"
  
  if [ ! -d "$DIR" ]; then
    echo "   ❌ Directory not found"
    ((FAILED++))
    continue
  fi
  
  cd "$DIR" || continue
  
  # Deploy using ADK (gs:// prefix required, absolutize_imports=false to avoid .venv hang)
  if adk deploy agent_engine \
    --project "$PROJECT" \
    --region "$LOCATION" \
    --staging_bucket "gs://$BUCKET" \
    --display_name "$NAME" \
    --absolutize_imports false \
    . > "/tmp/${NAME}_deploy.log" 2>&1; then
    
    echo "   ✅ $NAME deployed successfully"
    ((SUCCESS++))
  else
    echo "   ❌ $NAME deployment failed"
    echo "   📄 Log: /tmp/${NAME}_deploy.log"
    ((FAILED++))
  fi
  
  cd ..
  echo ""
done

echo "=================================================="
echo "✅ Successful: $SUCCESS"
echo "❌ Failed: $FAILED"
echo "📊 Total: $TOTAL"
echo ""
echo "Check deployed agents:"
echo "python3 check_deployed_agents.py"
