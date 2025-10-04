# 🚀 DEPLOY TO VERTEX AI AGENT ENGINE

## ✅ PRE-DEPLOYMENT CHECKLIST

Before deploying, ensure:
- [x] Multi-agent system tested (85% pass rate)
- [x] 8 specialist agents ready
- [x] 41 tools loaded
- [x] Self-coding working
- [ ] Firestore database created (5 min - do this first!)

---

## 📋 STEP 1: Create Firestore Database (5 min)

**This is REQUIRED for memory/notes:**

```bash
# Open the setup page
open "https://console.cloud.google.com/datastore/setup?project=studio-2416451423-f2d96"
```

**Then:**
1. Click "Create Database"
2. Select **"Firestore Native Mode"** (NOT Datastore)
3. Choose location: **us-central1**
4. Click "Create"
5. Wait 1-2 minutes for creation

**Test it works:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Save a note: Deployment ready!", "session_id": "test", "user_id": "deploy"}'
```

---

## 🚀 STEP 2: Deploy to Vertex AI Agent Engine

### Option A: Deploy with Cloud Run (Recommended)

```bash
# 1. Build container
cd /Users/liverichmedia/Agent\ master\ /genesis-agent/agent_backend

# 2. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8080

# Run
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# 3. Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.115.5
uvicorn[standard]==0.32.1
pydantic==2.10.3
google-cloud-aiplatform==1.76.0
google-cloud-firestore==2.19.0
google-cloud-storage==2.18.2
google-cloud-speech==2.28.0
google-cloud-texttospeech==2.18.0
google-cloud-videointelligence==2.13.5
httpx==0.28.1
twilio==9.3.7
python-multipart==0.0.20
EOF

# 4. Deploy to Cloud Run
gcloud run deploy cortex-os \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --project studio-2416451423-f2d96 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96
```

### Option B: Deploy with Vertex AI Agent Builder

```bash
# 1. Enable Agent Builder API
gcloud services enable agentbuilder.googleapis.com --project=studio-2416451423-f2d96

# 2. Create agent config
cat > agent_config.json << 'EOF'
{
  "displayName": "Cortex OS Multi-Agent System",
  "description": "8 Specialist AI Agents with 41 Tools",
  "agentId": "cortex-os-multi-agent",
  "llmConfig": {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.7
  },
  "tools": [
    {
      "customTool": {
        "endpoint": "https://cortex-os-XXXXX.run.app/api/chat",
        "method": "POST"
      }
    }
  ]
}
EOF

# 3. Deploy agent
gcloud alpha agent-builder agents create cortex-os-multi-agent \
  --config agent_config.json \
  --project studio-2416451423-f2d96 \
  --location us-central1
```

---

## 🌐 STEP 3: Set Up Public URL

After Cloud Run deployment, you'll get a URL like:
```
https://cortex-os-XXXXX-uc.a.run.app
```

**Update webhook endpoints:**

### For Telegram:
```bash
TELEGRAM_BOT_TOKEN="your_token_here"
CLOUD_RUN_URL="https://cortex-os-XXXXX-uc.a.run.app"

curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${CLOUD_RUN_URL}/webhook/telegram"
```

### For WhatsApp (Twilio):
1. Go to: https://console.twilio.com/
2. WhatsApp Sandbox Settings
3. Set webhook to: `https://cortex-os-XXXXX-uc.a.run.app/webhook/whatsapp`

---

## 🔐 STEP 4: Set Environment Variables

```bash
# In Cloud Run, add these env vars:
gcloud run services update cortex-os \
  --update-env-vars TELEGRAM_BOT_TOKEN=your_token,\
TWILIO_ACCOUNT_SID=your_sid,\
TWILIO_AUTH_TOKEN=your_token,\
GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96 \
  --region us-central1 \
  --project studio-2416451423-f2d96
```

---

## 🧪 STEP 5: Test Deployed System

```bash
# Set your Cloud Run URL
DEPLOY_URL="https://cortex-os-XXXXX-uc.a.run.app"

# Test health
curl "$DEPLOY_URL/api/health"

# Test agents
curl "$DEPLOY_URL/api/agents" | jq '.agents[].name'

# Test chat
curl -X POST "$DEPLOY_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hey! Are you deployed?",
    "session_id": "deploy_test",
    "user_id": "tester"
  }' | jq '.response'
```

---

## 📱 STEP 6: Connect Frontend

Update frontend to use deployed URL:

```javascript
// In your frontend .env
VITE_API_URL=https://cortex-os-XXXXX-uc.a.run.app
```

Or update `App.jsx`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'https://cortex-os-XXXXX-uc.a.run.app';
```

---

## ✅ DEPLOYMENT VERIFICATION

After deployment, verify:

1. **API accessible:** `curl https://your-url/api/health`
2. **Agents loaded:** `curl https://your-url/api/agents`
3. **Chat working:** Test via frontend
4. **Telegram working:** Message your bot
5. **WhatsApp working:** Send message to Twilio number

---

## 🎯 WHAT YOU'LL HAVE AFTER DEPLOYMENT

✅ **8 Specialist Agents** accessible worldwide
✅ **41 Tools** ready for any task
✅ **Multi-platform** (Web + Telegram + WhatsApp)
✅ **Self-coding** agent that can improve itself
✅ **Voice interface** for natural conversation
✅ **Zoom processing** for meetings
✅ **Performance metrics** for all agents

---

## 🆘 TROUBLESHOOTING

### Issue: "Database does not exist"
**Fix:** Create Firestore database (Step 1)

### Issue: "Permission denied"
**Fix:** Ensure service account has roles:
```bash
gcloud projects add-iam-policy-binding studio-2416451423-f2d96 \
  --member="serviceAccount:YOUR_SA@studio-2416451423-f2d96.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Issue: Telegram webhook fails
**Fix:** Ensure HTTPS URL, not HTTP

### Issue: Tools not loading
**Fix:** Check Cloud Run logs:
```bash
gcloud run logs read cortex-os --project studio-2416451423-f2d96
```

---

## 📊 COST ESTIMATE

**Monthly costs (estimated):**
- Cloud Run: $5-20 (based on usage)
- Vertex AI: $0.002/request (Gemini 2.0 Flash)
- Firestore: Free tier (up to 1GB)
- Storage: $0.02/GB
- Speech/Video APIs: Pay per use

**Total:** ~$10-50/month for moderate use

---

## 🎉 YOU'RE READY!

1. Create Firestore DB (5 min)
2. Run deployment command (10 min)
3. Set webhooks (5 min)
4. Test everything (5 min)

**Total time:** 25 minutes to full deployment! 🚀
