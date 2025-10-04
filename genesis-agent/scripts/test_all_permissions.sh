#!/bin/bash
# Test all IAM permissions for JAi Cortex OS

PROJECT_ID="studio-2416451423-f2d96"
LOCATION="us-central1"

echo "🧪 Testing JAi Cortex OS Permissions"
echo "====================================="
echo ""

PASSED=0
FAILED=0

# Function to test permission
test_permission() {
    SERVICE=$1
    COMMAND=$2
    DESCRIPTION=$3
    
    echo "Testing: $DESCRIPTION"
    echo "  Command: $COMMAND"
    
    if eval "$COMMAND" > /dev/null 2>&1; then
        echo "  ✅ PASS"
        ((PASSED++))
    else
        echo "  ❌ FAIL - Missing permission for $SERVICE"
        ((FAILED++))
    fi
    echo ""
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  VERTEX AI PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Vertex AI" \
    "gcloud ai models list --region=$LOCATION --project=$PROJECT_ID --limit=1" \
    "List Gemini models"

test_permission "Agent Engine" \
    "gcloud ai reasoning-engines list --region=$LOCATION --project=$PROJECT_ID --limit=1" \
    "List deployed agents"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  CLOUD STORAGE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Cloud Storage" \
    "gsutil ls gs://cortex_agent_staging" \
    "Access cortex_agent_staging bucket"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  FIRESTORE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Firestore" \
    "gcloud firestore databases list --project=$PROJECT_ID" \
    "Access Firestore databases"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  CLOUD TRACE PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Cloud Trace" \
    "gcloud trace list --project=$PROJECT_ID --limit=1" \
    "List traces"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  BIGQUERY PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "BigQuery" \
    "bq ls --project_id=$PROJECT_ID --max_results=1" \
    "List BigQuery datasets"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  CLOUD LOGGING PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Cloud Logging" \
    "gcloud logging logs list --project=$PROJECT_ID --limit=1" \
    "List logs"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  CLOUD MONITORING PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_permission "Cloud Monitoring" \
    "gcloud monitoring channels list --project=$PROJECT_ID --limit=1" \
    "List monitoring channels"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 ALL PERMISSIONS WORKING!"
    echo ""
    echo "You can now:"
    echo "  • Chat with JAi Cortex OS"
    echo "  • Call 24 specialist agents"
    echo "  • Upload files"
    echo "  • Save notes"
    echo "  • View traces"
    echo "  • Export to BigQuery"
    echo "  • Monitor performance"
else
    echo "⚠️  Some permissions missing."
    echo ""
    echo "Run this to grant missing permissions:"
    echo "  ./scripts/setup_all_iam_permissions.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

