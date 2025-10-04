# 🧠 Cognitive Modeling & Personalization

## Overview

JAi Cortex OS now includes **Cognitive Modeling** - an intelligent system that automatically learns your communication style, business contexts, and thinking patterns from every conversation.

---

## 🎯 What It Does

### **Automatic Conversation Capture**
Every message you send and every response JAi provides is automatically:
- **Saved** with semantic embeddings
- **Analyzed** for business context
- **Tagged** with communication patterns
- **Indexed** for future retrieval

### **Context Detection**
The system automatically detects:
- **Business Contexts**: Agency, Travel, Personal, Development, Technical
- **Communication Style**: Direct, Analytical, Creative
- **Key Entities**: Projects, systems, tools you work with
- **Message Patterns**: How you phrase requests

### **Adaptive Responses**
Over time, JAi will:
- Understand which "personality" you're in
- Adapt tone and detail level to your style
- Anticipate your needs based on past patterns
- Remember your preferences across sessions

---

## 🏗️ Architecture

### **Components:**

1. **`memory_service.py`** - Core cognitive engine
   - `detect_business_context()` - Analyzes conversation context
   - `auto_capture_conversation()` - Saves with intelligent tagging
   - `get_cognitive_profile()` - Generates user profile

2. **`cognitive_middleware.py`** - Integration layer
   - Bridges ADK and cognitive system
   - Handles auto-capture logic
   - Provides statistics

3. **Firestore Collections:**
   - `conversation_memory` - All conversations with metadata
   - `memory_embeddings` - Semantic vectors for search

---

## 🚀 Usage

### **Option 1: Manual Capture (Testing)**

Test the cognitive system with individual messages:

```python
from jai_cortex.memory_service import memory_service

# Manually capture a conversation
memory_service.auto_capture_conversation(
    user_id="default_user",
    session_id="test_session",
    user_message="Can you help me with my travel agency website?",
    agent_response="I'd be happy to help with your travel agency site..."
)

# Get your cognitive profile
profile = memory_service.get_cognitive_profile(user_id="default_user")
print(profile)
```

### **Option 2: Automatic Capture (Production)**

For full automation, integrate the cognitive middleware into your agent workflow.

**Method A: Background Service** (Coming Soon)
```bash
# Run alongside ADK server
python start_cognitive_capture.py
```

**Method B: Direct Integration** (Current)
The cognitive capture is automatically enabled. Every conversation through the ADK dev-ui is being captured with context detection.

---

## 📊 View Your Cognitive Profile

### **Using DatabaseExpert:**

Ask JAi:
```
Show me my cognitive profile from the last 30 days
```

DatabaseExpert will query the `conversation_memory` collection and analyze:
- Your most common business contexts
- Your communication style trends
- Key topics you discuss
- Interaction patterns

### **Programmatically:**

```python
from jai_cortex.memory_service import memory_service

# Get your profile
profile = memory_service.get_cognitive_profile(
    user_id="default_user",
    days=30  # Last 30 days
)

print(f"Total Conversations: {profile['total_conversations']}")
print(f"Primary Contexts: {profile['primary_contexts']}")
print(f"Communication Styles: {profile['communication_styles']}")
print(f"Key Topics: {profile['key_topics']}")
```

---

## 🔧 Configuration

### **Environment Variables:**

```bash
# Enable/disable cognitive capture
export COGNITIVE_CAPTURE=true

# Project and database
export GOOGLE_CLOUD_PROJECT=studio-2416451423-f2d96
export FIRESTORE_DATABASE=agent-master-database
```

### **Customize Context Detection:**

Edit `memory_service.py` → `detect_business_context()` to add your own keywords:

```python
# Add your own business contexts
agency_keywords = ['client', 'campaign', 'your-custom-keywords']
travel_keywords = ['destination', 'booking', 'your-travel-terms']
```

---

## 📈 What Gets Stored

### **Conversation Document Structure:**
```json
{
  "user_id": "default_user",
  "session_id": "abc123",
  "user_message": "Can you analyze my agency workflow?",
  "agent_response": "I'd be happy to analyze your workflow...",
  "timestamp": "2025-10-02T20:30:00Z",
  "metadata": {
    "type": "auto_captured_conversation",
    "auto_captured": true,
    "cognitive_analysis": {
      "contexts": {
        "agency": true,
        "travel": false,
        "personal": false,
        "development": false,
        "technical": false
      },
      "primary_context": "agency",
      "communication_style": "analytical",
      "entities": ["workflow_optimization"],
      "message_length": 8
    }
  }
}
```

---

## 🎯 Future Enhancements (Phase B)

### **Coming Next:**
- **Proactive Insights**: "I notice you ask about X every Monday - want to automate it?"
- **Context Switching Detection**: "Switching from agency to travel mode..."
- **Preference Learning**: Automatic adaptation of response style
- **Cross-Session Continuity**: "Continuing from where we left off last week..."
- **Multi-Business Management**: Separate cognitive profiles per business

---

## 🧪 Testing the System

### **Test 1: Context Detection**
```
Ask JAi: "I need help with a marketing campaign for a luxury hotel client"
```
→ Should detect: `agency=true`, `travel=true`, `style=analytical`

### **Test 2: Profile Analysis**
```
Ask JAi: "Show me my cognitive profile"
```
→ DatabaseExpert will analyze your patterns

### **Test 3: Adaptive Response**
After several conversations in "agency mode", ask a quick question.
→ JAi should respond in a more business-focused, direct tone

---

## 📝 Notes

- **Privacy**: All data stored in your own Firestore database
- **Control**: Enable/disable capture anytime with `COGNITIVE_CAPTURE` env var
- **Data Retention**: Set your own retention policies in Firestore
- **Extensibility**: Easy to add new contexts and patterns

---

## 🚀 Status

✅ **Phase A1: COMPLETE**
- Automatic conversation capture
- Context detection (5 contexts)
- Communication style analysis
- Cognitive profile generation

⏳ **Phase A2: IN PROGRESS**
- Context-aware response adaptation
- Pre-response profile loading

🔮 **Phase B: PLANNED**
- Full CognitiveModeler sub-agent
- Proactive pattern recognition
- Multi-personality management
Human: continue
