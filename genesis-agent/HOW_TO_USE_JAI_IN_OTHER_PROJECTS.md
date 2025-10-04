# 🚀 How to Use JAi Agent in Other GitHub Projects

## The Problem You Had Before

You tried to copy/paste JAi into another app and it didn't work because JAi has **dependencies** on:
- Knowledge base files
- Firestore database
- Autonomous engine modules
- Tool functions
- Environment variables

**Solution:** There are 3 ways to use JAi in other projects.

---

## ✅ METHOD 1: Import JAi as a Python Package (RECOMMENDED)

This is the cleanest way. Your other project imports JAi like any other library.

### Step 1: Make JAi Installable

```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"

# Create setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="jai-cortex",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-cloud-aiplatform",
        "google-cloud-firestore",
        "google-genai",
        "flask",
        "requests",
    ],
    python_requires=">=3.10",
)
EOF

# Install JAi in editable mode
pip install -e .
```

### Step 2: Use JAi in Your Other Project

```python
# In your other GitHub project
from jai_cortex_working import chat, root_agent
import asyncio

# Use JAi's chat function
async def my_app():
    response = await chat("Analyze this UI layout for me")
    print(response)

asyncio.run(my_app())
```

**Pros:**
- ✅ Clean separation
- ✅ Easy to update JAi without touching your other project
- ✅ Works anywhere Python works

**Cons:**
- JAi still needs access to:
  - Firestore database
  - Knowledge base file path
  - Environment variables

---

## ✅ METHOD 2: Deploy JAi to Vertex AI (USE IT AS AN API)

Deploy JAi once, call it from anywhere.

### Step 1: Deploy JAi

```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
adk deploy agent_engine . --project studio-2416451423-f2d96 --region us-central1 --staging_bucket gs://your-bucket
```

### Step 2: Call JAi from Your Other Project

```python
# In your other GitHub project
import requests
import google.auth
from google.auth.transport.requests import Request

# Get auth token
credentials, project = google.auth.default()
credentials.refresh(Request())
token = credentials.token

# Call deployed JAi
response = requests.post(
    "https://us-central1-aiplatform.googleapis.com/v1/projects/studio-2416451423-f2d96/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID:query",
    json={"query": "Analyze this UI layout"},
    headers={"Authorization": f"Bearer {token}"}
)

print(response.json())
```

**Pros:**
- ✅ Works from ANY language (Python, JavaScript, Go, etc.)
- ✅ No dependencies in your other project
- ✅ Centralized - one JAi serves all your apps

**Cons:**
- Requires internet connection
- Costs money (Vertex AI API calls)

---

## ✅ METHOD 3: Copy JAi Core Files (QUICKEST BUT MESSY)

Copy only what you need into your other project.

### Step 1: Copy Core Files

```bash
# In your other project directory
mkdir jai_agent

# Copy essential files
cp "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/jai_cortex_working.py" ./jai_agent/
cp -r "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/autonomous_engine" ./jai_agent/
cp "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/.env" ./jai_agent/
```

### Step 2: Update Paths

```python
# In your copied jai_cortex_working.py
# Change this line:
sys.path.insert(0, os.path.dirname(__file__))

# To this (adjust for your structure):
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'jai_agent'))
```

**Pros:**
- ✅ Fast to set up
- ✅ No deployment needed

**Cons:**
- ❌ Messy (duplicate code)
- ❌ Hard to update (must copy files again)
- ❌ Still needs Firestore and knowledge base files

---

## 🎬 VIDEO ANALYSIS - How to Use It

Once you have JAi in your project (via any method above), here's how to analyze videos:

### Upload Video and Analyze

```python
from jai_cortex_working import chat
import asyncio

async def analyze_app_ui():
    # You can either:
    # 1. Upload video to Google Cloud Storage
    # 2. Provide a video URL
    # 3. Upload directly via ADK dev-ui
    
    prompt = """
    I'm uploading a video of the Dream Machine app. 
    Please analyze:
    1. The overall layout structure
    2. Color scheme and typography
    3. Navigation patterns
    4. Key UI components
    5. How the video player is integrated
    6. Provide code structure to replicate this in my app
    """
    
    response = await chat(prompt)
    print(response)

asyncio.run(analyze_app_ui())
```

### OR Use ADK dev-ui (EASIEST)

1. Start your agent: `adk dev-ui`
2. Go to `http://localhost:8000`
3. **Upload your video** (there's an upload button)
4. Type: `Analyze this video and tell me how to build the same UI`

---

## 📦 What You Get From JAi

No matter which method you use, JAi gives you:

- ✅ **Cognitive profile** - Learns about your businesses
- ✅ **Knowledge base** - Remembers everything you teach it
- ✅ **Video/image analysis** - Analyzes UI layouts
- ✅ **Code generation** - Builds features for you
- ✅ **Research agent** - Proactively learns new topics
- ✅ **Web search** - Finds solutions online
- ✅ **All 24 specialist agents** - Database, Cloud, Code, etc.

---

## 🎯 RECOMMENDED PATH FOR YOU

**For your GitHub project:**

1. **Use METHOD 2** (Deploy to Vertex AI) - Most flexible
2. Call JAi as an API from your other project
3. Upload videos via Google Cloud Storage
4. JAi analyzes and returns structured code

**OR if you want it local:**

1. **Use METHOD 1** (Python package)
2. Install JAi in your other project's venv
3. Import and use directly

---

## Next Step: Test Video Analysis

**Right now:**
1. Restart your agent: `adk dev-ui`
2. Film your Dream Machine app video
3. Upload it to the agent
4. Ask: "Analyze this UI and give me code structure to replicate it"

**Want me to set this up for you? Tell me which method you prefer.**

