# 🧠 VERTEX AI SETUP - Get ALL 30+ Tools Working

This is the ONLY way to get the full super brain with all capabilities.

## ⏱️ TIME: 30-45 minutes
## 💰 COST: ~$5-20/month (pay as you go, only charged when you use it)

---

## 📋 **STEP-BY-STEP SETUP**

### **STEP 1: Enable Vertex AI** (5 minutes)

1. **Go to Google Cloud Console**: https://console.cloud.google.com
2. **Select your project**: `studio-2416451423-f2d96`
3. **Go to Vertex AI**: Search "Vertex AI" in top search bar
4. **Click "Enable API"**

### **STEP 2: Enable Billing** (REQUIRED - 5 minutes)

**Why needed**: Vertex AI requires billing enabled (even though there's a free tier)

1. **Go to Billing**: https://console.cloud.google.com/billing
2. **Link a billing account** (credit card required)
3. **Set up budget alerts**: Recommended $50/month alert

**Cost breakdown:**
- Gemini 2.5 Flash: $0.075 per 1M input tokens, $0.30 per 1M output tokens
- Typical usage: ~$5-10/month for moderate use
- First $300 in credits free for new GCP accounts

### **STEP 3: Authenticate** (10 minutes)

**Option A: Application Default Credentials (RECOMMENDED)**

```bash
# Run this in your terminal
gcloud auth application-default login

# This opens browser, you log in with your Google account
# Credentials saved automatically
```

**Option B: Service Account**

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Create service account
3. Grant role: "Vertex AI User"
4. Download JSON key
5. Set environment variable: `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

### **STEP 4: Update Environment Variables** (2 minutes)

Create/update `.env` file:

```bash
# FOR VERTEX AI (instead of API key)
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96
GOOGLE_CLOUD_LOCATION=us-central1

# Remove or comment out (not needed with Vertex AI)
# GOOGLE_API_KEY=...
```

### **STEP 5: Install Additional Libraries** (5 minutes)

```bash
cd /Users/liverichmedia/Agent\ master\ /genesis-agent/agent_backend

# Install Google Cloud libraries for all tools
pip install google-cloud-storage google-cloud-firestore google-cloud-videointelligence google-cloud-speech google-cloud-texttospeech
```

### **STEP 6: Initialize Firestore** (5 minutes)

**Why needed**: For agent memory, file indexing, workflow storage

1. **Go to Firestore**: https://console.cloud.google.com/firestore
2. **Click "Create Database"**
3. **Select "Native mode"**
4. **Choose location**: `us-central1` (same as Vertex AI)
5. **Start in production mode**

### **STEP 7: Create Cloud Storage Bucket** (3 minutes)

**Why needed**: For file storage (documents, videos, audio)

1. **Go to Cloud Storage**: https://console.cloud.google.com/storage
2. **Click "Create Bucket"**
3. **Name**: `cortex-os-data-YOUR-PROJECT-ID` (must be globally unique)
4. **Location**: `us-central1`
5. **Storage class**: Standard
6. **Update .env**: Add `GCS_BUCKET=cortex-os-data-YOUR-PROJECT-ID`

### **STEP 8: Test Everything** (5 minutes)

```bash
# Update backend to use Vertex AI
cd /Users/liverichmedia/Agent\ master\ /genesis-agent/agent_backend

# Kill old server
pkill -f "uvicorn"

# Start with Vertex AI
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96
export GOOGLE_CLOUD_LOCATION=us-central1
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Test the agent:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a new agent called Meeting Transcriber", "session_id": "test", "user_id": "user1"}'
```

**If you see a response (not an error) - ALL 30+ TOOLS NOW WORK! 🎉**

---

## ✅ **WHAT YOU GET AFTER SETUP**

### **File & Data Management** (7 tools) ✅
- Upload any file (docs, images, videos, audio)
- Automatic organization and tagging
- Vector search across all your data

### **Multimodal Analysis** (7 tools) ✅
- Analyze images and videos
- Transcribe audio
- Generate images
- Text-to-speech

### **Communication & Automation** (6 tools) ✅
- Send emails
- Manage calendar
- Create workflows
- Notifications

### **Web & Knowledge** (3 tools) ✅
- Real-time web search
- Web scraping
- API integration

### **Meta-Tools** (7 tools) ✅
- **CREATE NEW AGENTS** (the big one!)
- Deploy agents
- Self-debugging
- System monitoring

---

## 🚨 **COMMON ISSUES & FIXES**

### "Permission denied"
→ Run: `gcloud auth application-default login`

### "Quota exceeded"
→ Go to: https://console.cloud.google.com/apis/api/aiplatform.googleapis.com/quotas
→ Request quota increase (usually approved instantly)

### "Billing not enabled"
→ Must enable billing (required for Vertex AI)

### "Wrong region"
→ Make sure all services use same region: `us-central1`

---

## 📞 **NEED HELP?**

1. **Check Cloud Console**: https://console.cloud.google.com
2. **View logs**: `gcloud logging read --limit 50`
3. **Vertex AI docs**: https://cloud.google.com/vertex-ai/docs

---

**Once setup is complete, you'll have a TRUE SUPER BRAIN that can:**
- Ingest any data
- Analyze any content
- Automate any workflow
- CREATE OTHER AGENTS
- Self-improve and debug

**Ready to start? Let me know when you've completed each step!**


