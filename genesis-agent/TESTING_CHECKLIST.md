# JAi Cortex OS - Testing Checklist

**Server:** `http://localhost:8000/dev-ui/?app=jai_cortex`

---

## ✅ **Phase 1 & 2 Complete - What to Test:**

### **1. Health Check (NEW)**
**Try:** "Check system status" or "Run diagnostics"

**Should See:**
- ✅ Firestore: operational
- ✅ Cloud Storage: operational  
- ✅ Vision API: operational
- ✅ Speech API: operational
- ✅ All 8 tools: available

---

### **2. Infinite Memory (NEW - MOST IMPORTANT)**
**Try:** 
- First: "Save this note: Title 'Test Memory', content 'Testing infinite memory system'"
- Then: "Do you remember what note I just saved?"
- Or: "Search your memory for 'test memory'"

**Should See:**
- Agent finds the note you just saved
- Agent can recall past conversations
- This proves memory works!

---

### **3. Save Notes**
**Try:** "Save a note titled 'Roadmap Progress' with content 'Completed Phase 1 and Phase 2'"

**Should See:**
- ✅ Saved note: Roadmap Progress
- Uses ADK's native persistence

---

### **4. Web Search**
**Try:** "Search the web for Gemini 2.5 Pro features"

**Should See:**
- Search results (may be placeholder for now, that's fine)

---

### **5. Image Analysis (If you have an image)**
**Try:** Upload an image and say "Analyze this image"

**Should See:**
- Labels detected
- Objects/scenes identified
- Safe search rating

---

### **6. Video Analysis (If you have a small video <100MB)**
**Try:** Upload a video and say "Analyze this video"

**Should See:**
- Video labels/scenes
- Message: "temp files cleaned up to save costs"
- Video NOT stored permanently (cost optimization)

---

### **7. Transcribe Video (If you have a video with speech)**
**Try:** Upload a video with speech and say "Transcribe this video"

**Should See:**
- Full transcript of spoken words
- Word count

---

### **8. Text Extraction from Image (If you have text in an image)**
**Try:** Upload an image with text and say "Extract text from this image"

**Should See:**
- All text extracted via OCR

---

## **Most Important Tests (Priority Order):**

1. **✅ Health Check** - "Check system status"  
   → Confirms all services are operational

2. **🧠 Memory System** - "Search your memory for..." 
   → This is the game changer - proves infinite memory works

3. **💾 Save Notes** - "Save this note..."  
   → Proves persistence works

4. **🔍 Web Search** - "Search for..."  
   → Basic web connectivity

5. **📸 Image/Video** - Upload and analyze  
   → Proves media tools work (optional for now)

---

## **What Success Looks Like:**

✅ **Phase 1 Complete:**
- All tools respond without errors
- Health check shows all services operational
- Error handling is clear and helpful

✅ **Phase 2 Complete:**
- Memory search finds past conversations
- Agent can recall what you told it
- Never loses context across sessions

---

## **If Something Fails:**

Ask JAi: "Check system status" to diagnose which service has an issue.

The agent can now self-diagnose!

---

**Current Capabilities:**
- 8 working tools
- Infinite memory (saves everything)
- Self-diagnosis (health check)
- Cost-optimized (temp video processing)

**Next (Phase 3):**
- Connect 24 specialist agents
- Build coding team
- Add specialized knowledge bases

