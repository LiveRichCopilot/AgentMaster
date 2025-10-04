# ✅ API Key Configured! Now Complete Setup:

## 🔑 **WHAT YOU HAVE:**
✅ **API Key:** `AIzaSyCFbSXSYMdyViQfeQQwcJ3lVrm54kysnFE`

## 🎯 **WHAT YOU NEED:**
⏳ **Search Engine ID** (from programmablesearchengine.google.com)

---

## 📋 **GET YOUR SEARCH ENGINE ID:**

### **Option 1: Click this link**
👉 https://programmablesearchengine.google.com/controlpanel/all

### **Option 2: Step-by-step**
1. Go to: https://programmablesearchengine.google.com/
2. Click **"Get Started"** or **"Add"**
3. Fill in:
   - **Name:** `JAi Research Engine`
   - **What to search:** Toggle **"Search the entire web"** to **ON**
4. Click **"Create"**
5. **Copy the Search Engine ID** (looks like: `e4c8a9b6d12345678`)

---

## 🚀 **ONCE YOU HAVE THE SEARCH ENGINE ID:**

### **Super Easy Way:**
```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
./configure_search_api.sh
```
*(This script will ask for your Search Engine ID and configure everything)*

### **Manual Way:**
Edit `.env.search` and replace `YOUR_SEARCH_ENGINE_ID_HERE` with your actual ID:

```bash
export GOOGLE_SEARCH_API_KEY="AIzaSyCFbSXSYMdyViQfeQQwcJ3lVrm54kysnFE"
export GOOGLE_SEARCH_ENGINE_ID="YOUR_ID_HERE"  # ← Replace this
```

---

## ✨ **THEN START JAi:**

```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
./setup_web_search.sh
```

This will:
- ✅ Load your API credentials
- ✅ Restart JAi with Web Power-Up enabled
- ✅ Open at `http://localhost:8000/dev-ui/?app=jai_cortex`

---

## 🧪 **TEST IT:**

Ask JAi:
```
"Research the latest developments in quantum computing and give me a comprehensive brief with sources"
```

JAi will:
1. 🔍 Search Google for 5 relevant URLs
2. 📖 Read the full content from each
3. 🧠 Synthesize the findings with Gemini 2.5 Pro
4. 📚 Add citations to every claim
5. ✅ Return a comprehensive answer

**Takes about 15-30 seconds** (comprehensive research takes time!)

---

## 💡 **STUCK?**

**Problem:** "I can't find the Search Engine ID"
- After creating the search engine, click on it in the list
- Look for "Search engine ID" in the details
- It's usually in the format: `abc123def456:ghi789jkl012`

**Problem:** "The script isn't working"
- Make sure you're in the right directory
- Try: `cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"`
- Then: `./configure_search_api.sh`

**Problem:** "Still getting 'API not configured' error"
- Double-check both the API key and Search Engine ID are correct
- Make sure there are no extra spaces
- Restart JAi with `./setup_web_search.sh`

---

## 📊 **WHAT THIS GIVES YOU:**

| Before | After |
|--------|-------|
| Basic web search | Multi-source research |
| 1 search result snippet | 5 full articles analyzed |
| No citations | Full citations |
| Surface-level info | Deep, synthesized analysis |
| Like asking Google | Like asking Perplexity |

---

**🎉 You're almost there! Just need that Search Engine ID and you're good to go!**

**Let me know when you have it and I'll help configure everything!** 🚀

