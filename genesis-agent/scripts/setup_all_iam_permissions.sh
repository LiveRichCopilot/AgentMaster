#!/bin/bash
# Complete IAM Setup for JAi Cortex OS
# Sets up ALL permissions needed for the entire system

PROJECT_ID="studio-2416451423-f2d96"
LOCATION="us-central1"

echo "🔐 JAi Cortex OS - Complete IAM Setup"
echo "======================================"
echo ""
echo "Project: $PROJECT_ID"
echo "Location: $LOCATION"
echo ""

# Get current user
CURRENT_USER=$(gcloud config get-value account 2>/dev/null)

if [ -z "$CURRENT_USER" ]; then
    echo "❌ No gcloud account configured"
    echo "Run: gcloud auth login"
    exit 1
fi

echo "Setting up permissions for: $CURRENT_USER"
echo ""

# Function to grant role
grant_role() {
    ROLE=$1
    DESCRIPTION=$2
    
    echo "🔧 Granting: $DESCRIPTION"
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$CURRENT_USER" \
        --role="$ROLE" \
        --condition=None 2>&1 | grep -v "Updated IAM policy" | grep -v "bindings:" || true
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "   ✅ $DESCRIPTION"
    else
        echo "   ⚠️  May already be granted or need Owner permissions"
    fi
    echo ""
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  VERTEX AI PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/aiplatform.user" "Vertex AI User (use Gemini, call agents)"
grant_role "roles/aiplatform.admin" "Vertex AI Admin (manage Agent Engine)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  CLOUD STORAGE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/storage.admin" "Storage Admin (upload files, manage buckets)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  FIRESTORE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/datastore.user" "Firestore User (save notes, sessions)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  CLOUD TRACE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/cloudtrace.user" "Cloud Trace User (view traces)"
grant_role "roles/cloudtrace.admin" "Cloud Trace Admin (export, configure)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  BIGQUERY PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/bigquery.admin" "BigQuery Admin (export traces, run queries)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  CLOUD LOGGING PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/logging.admin" "Logging Admin (view logs, configure sinks)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  CLOUD MONITORING PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/monitoring.admin" "Monitoring Admin (create alerts, dashboards)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8️⃣  SERVICE USAGE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

grant_role "roles/serviceusage.serviceUsageConsumer" "Service Usage Consumer (call APIs)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ IAM SETUP COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 WHAT YOU CAN NOW DO:"
echo ""
echo "✅ Use Gemini 2.5 Pro (Vertex AI)"
echo "✅ Call 24 specialist agents on Agent Engine"
echo "✅ Upload files to Cloud Storage"
echo "✅ Save notes to Firestore"
echo "✅ View traces in Cloud Trace"
echo "✅ Export traces to BigQuery"
echo "✅ View logs in Cloud Logging"
echo "✅ Create monitoring alerts"
echo ""

echo "🧪 TEST YOUR SETUP:"
echo ""
echo "1. Send a chat message:"
echo "   Open: http://localhost:3000/chat"
echo ""
echo "2. View the trace:"
echo "   https://console.cloud.google.com/traces/list?project=$PROJECT_ID"
echo ""
echo "3. Check logs:"
echo "   https://console.cloud.google.com/logs?project=$PROJECT_ID"
echo ""
echo "4. Run test command:"
echo "   ./scripts/test_all_permissions.sh"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

