#!/bin/bash
# Setup Cloud Trace permissions for viewing agent traces

PROJECT_ID="studio-2416451423-f2d96"

echo "🔐 Setting up Cloud Trace Permissions"
echo "======================================"
echo ""

# Get current user
CURRENT_USER=$(gcloud config get-value account 2>/dev/null)

if [ -z "$CURRENT_USER" ]; then
    echo "❌ No gcloud account configured"
    echo "Run: gcloud auth login"
    exit 1
fi

echo "Current user: $CURRENT_USER"
echo "Project: $PROJECT_ID"
echo ""

# Grant Cloud Trace User role
echo "Granting Cloud Trace User role..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$CURRENT_USER" \
    --role="roles/cloudtrace.user" \
    --condition=None 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Cloud Trace User role granted"
else
    echo "⚠️  Role may already be granted or you need Owner/Editor permissions"
fi

echo ""
echo "📊 You can now view traces at:"
echo "https://console.cloud.google.com/traces/list?project=$PROJECT_ID"
echo ""
echo "🧪 Test by sending a chat request:"
echo 'curl -X POST http://localhost:8000/api/chat \\'
echo '  -H "Content-Type: application/json" \\'
echo '  -d '"'"'{"message": "Test tracing", "session_id": "test", "user_id": "test"}'"'"

