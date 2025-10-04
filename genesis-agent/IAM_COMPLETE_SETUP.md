# 🔐 Complete IAM Setup for JAi Cortex OS

## Overview

Your JAi Cortex OS uses **8 Google Cloud services**. Each requires specific IAM permissions. This guide ensures you have ALL necessary permissions.

---

## 🚀 Quick Setup (Recommended)

### One Command to Grant Everything:
```bash
cd "/Users/liverichmedia/Agent master /genesis-agent"
./scripts/setup_all_iam_permissions.sh
```

This grants you permissions for:
- ✅ Vertex AI (Gemini, Agent Engine)
- ✅ Cloud Storage (file uploads)
- ✅ Firestore (notes, sessions)
- ✅ Cloud Trace (monitoring)
- ✅ BigQuery (trace analytics)
- ✅ Cloud Logging (logs)
- ✅ Cloud Monitoring (alerts)
- ✅ Service Usage (API calls)

### Test Everything Works:
```bash
./scripts/test_all_permissions.sh
```

---

## 📋 Required Permissions by Service

### 1. **Vertex AI** (Core AI Services)

**What it's for:**
- Using Gemini 2.5 Pro
- Calling 24 deployed specialist agents
- Agent Engine runtime

**Roles needed:**
```bash
# Use Gemini and call agents
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/aiplatform.user"

# Manage Agent Engine (deploy, update agents)
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/aiplatform.admin"
```

**Test it:**
```bash
# List deployed agents
gcloud ai reasoning-engines list \
    --region=us-central1 \
    --project=studio-2416451423-f2d96
```

---

### 2. **Cloud Storage** (File Management)

**What it's for:**
- Uploading files via `upload_file` tool
- Storing media in `cortex_agent_staging` bucket
- Agent deployment staging

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/storage.admin"
```

**Test it:**
```bash
# List bucket contents
gsutil ls gs://cortex_agent_staging
```

---

### 3. **Firestore** (Database for Notes & Sessions)

**What it's for:**
- Saving notes via `save_note` tool
- Searching notes via `search_notes` tool
- Storing conversation sessions
- Agent memory

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/datastore.user"
```

**Test it:**
```bash
# List Firestore databases
gcloud firestore databases list --project=studio-2416451423-f2d96
```

---

### 4. **Cloud Trace** (Request Monitoring)

**What it's for:**
- Viewing agent delegation traces
- Monitoring tool execution times
- Analyzing request performance
- Tracking specialist agent calls

**Roles needed:**
```bash
# View traces
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/cloudtrace.user"

# Export and configure
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/cloudtrace.admin"
```

**Test it:**
```bash
# List recent traces
gcloud trace list --project=studio-2416451423-f2d96 --limit=5
```

**View in console:**
https://console.cloud.google.com/traces/list?project=studio-2416451423-f2d96

---

### 5. **BigQuery** (Trace Analytics & Long-term Storage)

**What it's for:**
- Exporting traces for analysis
- Long-term trace storage (>30 days)
- SQL queries on agent usage patterns
- Performance analytics

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/bigquery.admin"
```

**Test it:**
```bash
# List datasets
bq ls --project_id=studio-2416451423-f2d96
```

---

### 6. **Cloud Logging** (Application Logs)

**What it's for:**
- Viewing agent logs
- Debugging errors
- Audit trails
- Log-based metrics

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/logging.admin"
```

**Test it:**
```bash
# List recent logs
gcloud logging logs list --project=studio-2416451423-f2d96 --limit=5
```

**View in console:**
https://console.cloud.google.com/logs?project=studio-2416451423-f2d96

---

### 7. **Cloud Monitoring** (Alerts & Dashboards)

**What it's for:**
- Creating latency alerts
- Setting up error rate monitoring
- Building performance dashboards
- Notification channels

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/monitoring.admin"
```

**Test it:**
```bash
# List alert policies
gcloud monitoring policies list --project=studio-2416451423-f2d96
```

**View in console:**
https://console.cloud.google.com/monitoring?project=studio-2416451423-f2d96

---

### 8. **Service Usage** (API Access)

**What it's for:**
- Calling Google Cloud APIs
- Service quota management
- API enablement

**Roles needed:**
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/serviceusage.serviceUsageConsumer"
```

**Test it:**
```bash
# List enabled APIs
gcloud services list --enabled --project=studio-2416451423-f2d96 | head -10
```

---

## 🔐 Service Account Setup (Optional - For Production)

If deploying to production, create a service account with these roles:

```bash
# Create service account
gcloud iam service-accounts create jai-cortex-os \
    --display-name="JAi Cortex OS Service Account" \
    --project=studio-2416451423-f2d96

# Grant all necessary roles
SA_EMAIL="jai-cortex-os@studio-2416451423-f2d96.iam.gserviceaccount.com"

for role in \
    "roles/aiplatform.user" \
    "roles/storage.admin" \
    "roles/datastore.user" \
    "roles/cloudtrace.agent" \
    "roles/logging.logWriter" \
    "roles/monitoring.metricWriter"
do
    gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
        --member="serviceAccount:$SA_EMAIL" \
        --role="$role"
done

# Download key
gcloud iam service-accounts keys create ~/jai-cortex-key.json \
    --iam-account=$SA_EMAIL

# Use in application
export GOOGLE_APPLICATION_CREDENTIALS=~/jai-cortex-key.json
```

---

## 🧪 Comprehensive Permission Test

### Test ALL Permissions:
```bash
./scripts/test_all_permissions.sh
```

### Expected Output:
```
Testing: List Gemini models
  ✅ PASS

Testing: List deployed agents
  ✅ PASS

Testing: Access cortex_agent_staging bucket
  ✅ PASS

Testing: Access Firestore databases
  ✅ PASS

Testing: List traces
  ✅ PASS

Testing: List BigQuery datasets
  ✅ PASS

Testing: List logs
  ✅ PASS

Testing: List monitoring channels
  ✅ PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 TEST RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed: 8
❌ Failed: 0

🎉 ALL PERMISSIONS WORKING!
```

---

## 🚨 Troubleshooting

### "Permission Denied" Errors

**Error**: `403 Forbidden` or `Permission denied`

**Solution**:
```bash
# Re-run IAM setup
./scripts/setup_all_iam_permissions.sh

# Or grant specific role manually
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/ROLE_NAME"
```

### "Project Not Found"

**Error**: `Project [studio-2416451423-f2d96] not found`

**Solution**:
```bash
# Set default project
gcloud config set project studio-2416451423-f2d96

# Verify
gcloud config get-value project
```

### "Not Authenticated"

**Error**: `You do not currently have an active account selected`

**Solution**:
```bash
# Login
gcloud auth login

# Set application default credentials
gcloud auth application-default login
```

---

## 📊 Permission Summary Table

| Service | Role | Purpose | Required For |
|---------|------|---------|--------------|
| Vertex AI | `aiplatform.user` | Use Gemini, call agents | Core functionality |
| Vertex AI | `aiplatform.admin` | Manage Agent Engine | Deploy agents |
| Cloud Storage | `storage.admin` | Upload files | `upload_file` tool |
| Firestore | `datastore.user` | Save/search notes | `save_note`, `search_notes` |
| Cloud Trace | `cloudtrace.user` | View traces | Monitoring |
| Cloud Trace | `cloudtrace.admin` | Export traces | BigQuery export |
| BigQuery | `bigquery.admin` | Query analytics | Trace analysis |
| Cloud Logging | `logging.admin` | View logs | Debugging |
| Cloud Monitoring | `monitoring.admin` | Create alerts | Performance monitoring |
| Service Usage | `serviceusage.serviceUsageConsumer` | Call APIs | All services |

---

## ✅ Verification Checklist

After running setup scripts, verify:

- [ ] Can send chat messages
- [ ] Can see tool calls in responses
- [ ] Can view traces in Cloud Trace
- [ ] Can save notes to Firestore
- [ ] Can upload files to Cloud Storage
- [ ] Can view logs in Cloud Logging
- [ ] Can create alerts in Cloud Monitoring
- [ ] Can export traces to BigQuery

---

## 🎯 Next Steps

1. **Run setup**: `./scripts/setup_all_iam_permissions.sh`
2. **Test permissions**: `./scripts/test_all_permissions.sh`
3. **Send test message**: Open http://localhost:3000/chat
4. **View trace**: https://console.cloud.google.com/traces/list?project=studio-2416451423-f2d96
5. **Check logs**: https://console.cloud.google.com/logs?project=studio-2416451423-f2d96

---

## 📚 Official Documentation

- [IAM Overview](https://cloud.google.com/iam/docs/overview)
- [Vertex AI IAM](https://cloud.google.com/vertex-ai/docs/general/access-control)
- [Cloud Trace IAM](https://cloud.google.com/trace/docs/iam)
- [Storage IAM](https://cloud.google.com/storage/docs/access-control/iam)
- [Firestore IAM](https://cloud.google.com/firestore/docs/security/iam)
- [BigQuery IAM](https://cloud.google.com/bigquery/docs/access-control)

---

**All IAM permissions documented and automated for JAi Cortex OS** ✅

