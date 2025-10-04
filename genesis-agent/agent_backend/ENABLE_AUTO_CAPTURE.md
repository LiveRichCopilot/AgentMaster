# 🧠 Enable Auto-Capture of ALL Conversations

## Current Status
- ✅ Auto-capture code exists (`cognitive_middleware.py`)
- ⚠️ May not be fully wired into the main agent
- ⚠️ Cognitive profile has Firestore index issue (needs restart)

---

## Step 1: Restart Your Agent (Load Fixed Cognitive Profile)

**In your terminal where `adk dev-ui` is running:**

```bash
# Press Ctrl+C to stop the agent

# Then restart:
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
adk dev-ui
```

**This loads the FIXED cognitive profile code that doesn't need the Firestore index.**

---

## Step 2: Verify Auto-Capture is Enabled

The auto-capture should be ON by default, but let's verify:

```bash
# Check if environment variable is set
echo $COGNITIVE_CAPTURE

# If it's not set or shows "false", enable it:
export COGNITIVE_CAPTURE=true
```

---

## Step 3: Test That Conversations Are Being Saved

### Test A: Have a Conversation

Go to `http://localhost:8000` and say:

```
Hello JAi, I want you to remember that I prefer visual explanations before code. 
I work on my Switch app at https://github.com/LiveRichCopilot/switch.git 
and I think in workflows: video → understanding → code.
```

### Test B: Check Firestore

1. Go to https://console.firebase.google.com
2. Navigate to your project: `studio-2416451423-f2d96`
3. Click "Firestore Database"
4. Select database: `agent-master-database`
5. Open collection: `conversation_memory`

**You should see:**
- New documents appearing with each conversation
- Fields: `user_message`, `agent_response`, `timestamp`, `metadata`
- Metadata includes: `cognitive_analysis` with contexts, style, entities

---

## Step 4: Test Cognitive Profile (See If It Learned)

After having a few conversations, ask:

```
Show me my cognitive profile from the last 7 days
```

**You should see:**
- Total conversations analyzed
- Your primary contexts (development, Switch app, etc.)
- Your communication style (visual, directive, etc.)
- Key topics you've discussed

---

## What Auto-Capture Does

**Every conversation turn:**
1. Automatically saved to Firestore `conversation_memory`
2. Analyzed for business contexts (agency, travel, development)
3. Communication style detected (visual, directive, technical)
4. Key topics and entities extracted
5. Embeddings generated for semantic search

**This means JAi learns:**
- ✅ "This user uploads videos and says 'breakdown' → analyze video first"
- ✅ "This user has Switch app on GitHub at this URL"
- ✅ "This user thinks: visual → understanding → code"
- ✅ "This user works on travel booking, agency sites, and AI apps"

---

## How to Verify It's Working

### Check 1: Firestore Has New Conversations

```bash
# Quick check from terminal
python3 -c "
from google.cloud import firestore
db = firestore.Client(project='studio-2416451423-f2d96', database='agent-master-database')
docs = db.collection('conversation_memory').limit(5).stream()
count = 0
for doc in docs:
    count += 1
    data = doc.to_dict()
    print(f'{count}. {data.get(\"user_message\", \"\")[:50]}...')
print(f'Total found: {count}')
"
```

### Check 2: Cognitive Profile Works

```bash
# Test cognitive profile
python3 -c "
from jai_cortex.memory_service import memory_service
profile = memory_service.get_cognitive_profile(user_id='default_user', days=7)
print(f'Conversations: {profile[\"total_conversations\"]}')
print(f'Contexts: {profile[\"primary_contexts\"]}')
print(f'Styles: {profile[\"communication_styles\"]}')
"
```

---

## What If Auto-Capture Isn't Working?

### Issue 1: Conversations Not Saving

**Solution:** Add explicit capture to the agent

Edit `/Users/liverichmedia/Agent master /genesis-agent/agent_backend/jai_cortex_working.py`:

```python
# At the top, add:
from jai_cortex.cognitive_middleware import cognitive_middleware

# In the chat function, after getting the response, add:
async def chat(message: str, user_id: str = "default_user", session_id: str = "default_session"):
    # ... existing code ...
    
    response = model.generate_content(...)
    
    # 🔥 ADD THIS - Auto-capture the conversation
    cognitive_middleware.capture_conversation(
        user_id=user_id,
        session_id=session_id,
        user_message=message,
        agent_response=response.text
    )
    
    return response.text
```

### Issue 2: Cognitive Profile Still Fails

If you still see the Firestore index error after restarting:

**The fix IS in the code** (we verified it). The issue is the running agent hasn't reloaded.

**Solution:** 
1. Completely stop the agent (Ctrl+C)
2. Wait 5 seconds
3. Restart: `adk dev-ui`
4. Test again

---

## Success Criteria

**You'll know it's working when:**

1. ✅ Every conversation appears in Firestore `conversation_memory`
2. ✅ `Show me my cognitive profile` returns your actual conversations
3. ✅ The profile shows YOUR contexts (Switch, development, visual thinking)
4. ✅ JAi starts to understand your communication patterns better

---

## Next Step

**RIGHT NOW:**
1. Stop your agent (Ctrl+C)
2. Restart it (`adk dev-ui`)
3. Have a conversation
4. Check Firestore to see if it saved
5. Test: `Show me my cognitive profile`

**Report back:** Did conversations save? Does cognitive profile work now?

