# 🚀 Quick Start: Enable Web Power-Up

## ⏱️ 5-Minute Setup

### **Step 1: Get Your API Key** (2 minutes)

You're already on the right page! Now:

1. In the **left sidebar**, click **"Credentials"**
2. Click **"+ Create Credentials"** at the top
3. Select **"API Key"**
4. **Copy the key** (it looks like: `AIzaSyABC123...`)
5. *(Optional)* Click "Restrict Key" → Select "Custom Search API" → Save

---

### **Step 2: Create Search Engine** (2 minutes)

1. Go to: **https://programmablesearchengine.google.com/**
2. Sign in with your Google account
3. Click **"Add"** or **"Get Started"**
4. Fill in:
   - **Name:** "JAi Research Engine"
   - **What to search:** Toggle "Search the entire web" **ON**
5. Click **"Create"**
6. **Copy the Search engine ID** (looks like: `a1b2c3d4e5f6g7h8i`)

---

### **Step 3: Configure JAi** (1 minute)

Open this file in your editor:
```
genesis-agent/agent_backend/.env.search
```

Replace the placeholders with your actual values:
```bash
export GOOGLE_SEARCH_API_KEY="AIzaSyABC123..."  # ← Your key from Step 1
export GOOGLE_SEARCH_ENGINE_ID="a1b2c3d4e5..."  # ← Your ID from Step 2
```

**Save the file.**

---

### **Step 4: Start JAi with Web Power-Up** (30 seconds)

Run this command:
```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
./setup_web_search.sh
```

**That's it!** 🎉

---

## 🧪 **Test It:**

Go to: `http://localhost:8000/dev-ui/?app=jai_cortex`

Try asking:
```
"Research the latest developments in AI agents and give me a comprehensive brief with sources"
```

JAi will:
1. 🔍 Search 5 sources
2. 📖 Read full content from each
3. 🧠 Synthesize findings
4. 📚 Add citations
5. ✅ Return comprehensive answer

---

## 💡 **Pro Tips:**

**For Research Queries, Use:**
- "Research X and give me a brief"
- "What are the latest developments in X?"
- "Compare X vs Y with multiple sources"

**For Quick Facts, JAi Will Use:**
- `simple_search` (faster, no deep analysis)

JAi automatically picks the right tool! 🧠

---

## 🐛 **Troubleshooting:**

**Problem:** Script says "API key not configured"
- **Fix:** Make sure you replaced `YOUR_API_KEY_HERE` in `.env.search`

**Problem:** "No search results"
- **Fix:** Double-check both the API key and Search Engine ID are correct

**Problem:** "Sites blocking access"
- **Fix:** This is normal for some sites. JAi will use the 3-4 sources that work.

---

## 📊 **What's Different Now:**

| Before | After |
|--------|-------|
| Simple web search | Multi-source research |
| 1 snippet | 5 full articles |
| No citations | Full citations |
| Surface info | Deep analysis |

**You now have Perplexity-level research in JAi!** 🚀

---

## 💰 **Cost:**

- **First 100 searches/day:** FREE
- **After that:** $5 per 1000 queries

For typical usage (10-20 research queries/day), this stays **FREE**.

---

**Need help? Look at:**
- `WEB_POWER_UP_SETUP.md` - Detailed technical guide
- `WEB_POWER_UP_SPEC.md` - Architecture documentation

**Ready to research! 🌐**

