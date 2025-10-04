# 🧪 TEST IT YOURSELF - NO BULLSHIT

**You don't trust automated tests? GOOD. Test it yourself.**

---

## Step 1: Start Your Agent

```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
adk dev-ui
```

**Wait for:** `Server running at http://localhost:8000`

---

## Step 2: Open Your Agent

**Go to:** `http://localhost:8000`

You'll see the ADK dev-ui with a chat interface.

---

## Step 3: Test Each Capability YOURSELF

### ✅ TEST 1: Cognitive Profile (Learning About YOU)

**What you type:**
```
Show me my cognitive profile from the last 30 days
```

**What you should see:**
- How many conversations I've analyzed
- Your primary business contexts (development, travel, agency, etc.)
- Your communication style
- Key topics you talk about

**If it fails:** You'll see an error message

---

### ✅ TEST 2: Learn From Error

**What you type:**
```
Learn from this error: "Flask app crashed with 500 error". The solution was "Added error handling to the route". Context: "Building travel booking API"
```

**What you should see:**
```
✅ Learned from error. I will remember this solution.
```

**Verify it saved:**
```
Search my knowledge for "Flask app crashed"
```

**You should see:** The error you just taught me

---

### ✅ TEST 3: Research Topic (Proactive Learning)

**What you type:**
```
Research "Python async best practices" and save it to your knowledge base
```

**What you should see:**
- "Researching..."
- List of topics learned
- "✅ Research complete"
- Knowledge base summary

---

### ✅ TEST 4: Web Search for Solution

**What you type:**
```
Search the web for a solution to "How to handle CORS in Flask API"
```

**What you should see:**
- Real Google search results
- URLs from Stack Overflow, documentation, etc.
- Synthesized solution

---

### ✅ TEST 5: Code Verification

**What you type:**
```
Verify this code quality:
def hello():
    return "Hello World"
```

**What you should see:**
```
✅ Code verification complete
```

---

## What If It Doesn't Work?

**If ANY of these fail:**

1. Check the terminal where `adk dev-ui` is running
2. Look for error messages
3. Take a screenshot
4. Send it to me

**I will NOT tell you "it should work" anymore. You test it. If it fails, I fix it.**

---

## What About Auto-Saving Everything?

**Current Status:**
- ✅ Notes are auto-saved (you can verify in Firestore `conversation_memory` collection)
- ⚠️  Regular conversations need auto-capture enabled

**To enable auto-capture of ALL conversations:**

```bash
export COGNITIVE_CAPTURE=true
```

Then restart the agent.

**Verify in Firestore:**
1. Go to https://console.firebase.google.com
2. Navigate to `agent-master-database`
3. Open `conversation_memory` collection
4. You should see EVERY conversation

---

## What About Google Cloud Storage?

**Current Status:**
- Knowledge is stored in: `/genesis-agent/agent_backend/autonomous_engine/jai_cortex_knowledge.json`
- Conversations are stored in: Firestore `conversation_memory`

**To move to GCS buckets:**
That's the next step - we need to:
1. Create a GCS bucket for your knowledge base
2. Create a GCS bucket for conversation history
3. Update all agents to read/write from GCS instead of local files

**But first: TEST WHAT WE HAVE. If these 5 tests pass, THEN we move to GCS.**

---

## DON'T TRUST ME - TRUST YOUR OWN TESTING

Start the agent. Test it yourself. If it works, great. If it doesn't, screenshot the error and I'll fix it.

**No more "it should work" - only "I tested it and here's what happened".**

