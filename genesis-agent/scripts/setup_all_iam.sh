#!/bin/bash

# Complete IAM Setup for JAi Cortex
# Sets ALL necessary permissions for Vertex AI, Storage, Speech, Vision, etc.

PROJECT_ID="studio-2416451423-f2d96"
SERVICE_ACCOUNT="studio-2416451423-f2d96@appspot.gserviceaccount.com"

echo "🔐 Setting up ALL IAM permissions for JAi Cortex..."
echo "Project: $PROJECT_ID"
echo "Service Account: $SERVICE_ACCOUNT"
echo ""

# 1. Vertex AI Permissions
echo "📌 Setting Vertex AI permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/aiplatform.user" \
    --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/aiplatform.admin" \
    --condition=None

# 2. Cloud Storage Permissions
echo "📌 Setting Cloud Storage permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.admin" \
    --condition=None

# 3. Speech-to-Text Permissions
echo "📌 Setting Speech-to-Text permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/speech.admin" \
    --condition=None

# 4. Vision API Permissions
echo "📌 Setting Vision API permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/cloudvisionai.admin" \
    --condition=None

# 5. Video Intelligence Permissions
echo "📌 Setting Video Intelligence permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/videointelligence.admin" \
    --condition=None

# 6. Firestore Permissions
echo "📌 Setting Firestore permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/datastore.user" \
    --condition=None

# 7. Service Account Token Creator (for calling other services)
echo "📌 Setting Service Account Token Creator..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountTokenCreator" \
    --condition=None

# 8. Service Usage Consumer (for API access)
echo "📌 Setting Service Usage Consumer..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/serviceusage.serviceUsageConsumer" \
    --condition=None

echo ""
echo "✅ ALL IAM permissions set!"
echo ""
echo "To verify, run:"
echo "  gcloud projects get-iam-policy $PROJECT_ID --flatten='bindings[].members' --filter='bindings.members:$SERVICE_ACCOUNT'"
