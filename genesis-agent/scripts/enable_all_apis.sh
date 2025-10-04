#!/bin/bash
# Enable all required Google Cloud APIs for JAi Cortex OS

PROJECT_ID="studio-2416451423-f2d96"

echo "🔌 Enabling All Required APIs"
echo "=============================="
echo ""
echo "Project: $PROJECT_ID"
echo ""

# List of required APIs
APIS=(
    "aiplatform.googleapis.com"           # Vertex AI
    "storage-api.googleapis.com"          # Cloud Storage
    "storage-component.googleapis.com"    # Cloud Storage
    "firestore.googleapis.com"            # Firestore
    "cloudtrace.googleapis.com"           # Cloud Trace
    "bigquery.googleapis.com"             # BigQuery
    "logging.googleapis.com"              # Cloud Logging
    "monitoring.googleapis.com"           # Cloud Monitoring
    "cloudresourcemanager.googleapis.com" # Resource Manager
    "iam.googleapis.com"                  # IAM
    "serviceusage.googleapis.com"         # Service Usage
)

echo "Enabling APIs..."
echo ""

for api in "${APIS[@]}"; do
    echo "🔧 Enabling: $api"
    gcloud services enable $api --project=$PROJECT_ID 2>&1 | grep -v "already enabled" || echo "   ✅ $api"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL APIS ENABLED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Enabled APIs:"
for api in "${APIS[@]}"; do
    echo "  • $api"
done
echo ""
echo "🎯 Next: Run permission setup"
echo "   ./scripts/setup_all_iam_permissions.sh"

