# 🔄 Workflow & Integration Tools Reference

**Complete documentation of all workflow orchestration and integration tools**

Last Updated: October 6, 2025
Total Tools: 146 (20 workflow + integration tools)

---

## 📁 File Structure

```
genesis-agent/agent_backend/jai_cortex/
├── workflow_orchestrator.py          (17K) - 4 workflow tools
├── switch_integration_bridge.py      (19K) - 6 integration tools
├── switch_app_file_manager.py        (13K) - 6 file management tools
├── switch_app_agent_builder.py       (16K) - 4 agent builder tools
└── workflow_tools.py                 (9.8K) - Legacy workflow tools
```

---

## 🔄 WORKFLOW ORCHESTRATOR (4 tools)
**File:** `workflow_orchestrator.py`

### 1. `build_switch_app_agent_workflow`
**Purpose:** Complete Switch app setup in one workflow

**What it does:**
1. Creates user agent
2. Creates customer service agent
3. Sets up file storage
4. Integrates NotebookLM
5. Generates UI code
6. Deploys everything

**Parameters:**
- `user_id`: User's ID
- `user_name`: User's name
- `business_name`: Business name
- `business_description`: Business description

**Returns:** Complete setup results with all agent IDs and URLs

**Example:**
```python
"Build a complete Switch app for user John with business 'Acme Corp'"
```

---

### 2. `upload_and_process_file_workflow`
**Purpose:** Smart file upload with automatic processing

**What it does:**
1. Uploads file to Cloud Storage
2. Processes with Vision API (if image)
3. Extracts text (if document)
4. Creates collection suggestion
5. Updates user's file index

**Parameters:**
- `file_content`: File content (base64 or path)
- `file_name`: File name
- `user_id`: User ID
- `file_type`: File type (image, video, document, audio)
- `auto_analyze`: Whether to auto-analyze

**Returns:** Upload result with analysis and collection suggestions

**Example:**
```python
"Upload this image and analyze it automatically"
```

---

### 3. `deploy_agent_to_cloud_workflow`
**Purpose:** Full deployment pipeline with validation

**What it does:**
1. Verifies agent exists
2. Generates deployment config
3. Creates Dockerfile
4. Builds container
5. Deploys to Cloud Run
6. Validates deployment
7. Returns live URL

**Parameters:**
- `agent_id`: Agent to deploy
- `deployment_name`: Cloud Run service name

**Returns:** Deployment results with live URL

**Example:**
```python
"Deploy my customer service agent to Cloud Run"
```

---

### 4. `intelligent_tool_chain`
**Purpose:** AI-powered tool orchestration - THE SMART ONE! 🧠

**What it does:**
- Analyzes your goal
- Automatically determines which tools to chain
- Calls them in the right sequence
- Returns complete results

**Supported workflows:**
- "Build Switch app" → Full app setup
- "Upload file" → Upload + analyze + organize
- "Deploy agent" → Verify + build + deploy + validate
- "Create agent" → CodeMaster → CloudExpert → Deploy
- "Fix deployment" → Diagnose → Fix → Redeploy

**Parameters:**
- `goal`: What you want to accomplish (natural language)
- `context`: Additional context (dict)

**Returns:** Results from entire tool chain

**Example:**
```python
"Build a chatbot for Switch app with file upload capabilities"
```

---

## 🌉 SWITCH INTEGRATION BRIDGE (6 tools)
**File:** `switch_integration_bridge.py`

### 5. `deploy_feature_to_switch`
**Purpose:** Deploy a feature from Agent Master to Switch app

**What it does:**
1. Saves feature code to Firestore
2. Determines target file path
3. Creates deployment instructions
4. Tracks feature status

**Parameters:**
- `feature_name`: Name of the feature (e.g., "ai-chat-widget")
- `feature_type`: Type (component, page, api, function, hook, util)
- `code_content`: The code to deploy

**Returns:** Deployment instructions and tracking info

**Example:**
```python
"Deploy this React component to Switch app"
```

---

### 6. `deploy_to_switch_firebase`
**Purpose:** Push feature live to Switch Firebase hosting

**What it does:**
1. Gets feature from Firestore
2. Calls CloudExpert to deploy
3. Updates deployment status
4. Returns live URL

**Parameters:**
- `feature_name`: Name of the feature to deploy
- `auto_deploy`: Whether to auto-deploy or just prepare

**Returns:** Deployment result with live URL

**Example:**
```python
"Deploy the ai-chat-widget feature to Firebase"
```

---

### 7. `sync_agent_to_switch`
**Purpose:** Sync an Agent Master agent to Switch app

**Integration types:**
- **chatbot**: React component with UI
- **api**: Next.js API endpoint
- **background_worker**: Firebase Function

**What it does:**
1. Gets agent config
2. Generates integration code (chatbot/API/worker)
3. Deploys to Switch
4. Returns integration details

**Parameters:**
- `agent_id`: Agent to sync
- `integration_type`: How to integrate (chatbot, api, background_worker)

**Returns:** Integration result with endpoints/URLs

**Example:**
```python
"Sync my customer service agent as a chatbot in Switch"
```

---

### 8. `create_switch_feature_from_prompt` ✨
**Purpose:** THE MAGIC TOOL - Natural language → Switch feature

**What it does:**
1. Calls CodeMaster to generate code from description
2. Deploys to Switch automatically
3. Returns live URL

**Parameters:**
- `feature_description`: What you want to build (natural language)
- `target_location`: Where in Switch (component, page, api, function)

**Returns:** Complete feature with code and deployment

**Example:**
```python
"Build a video upload widget with drag-and-drop for Switch"
```

---

### 9. `get_switch_app_status`
**Purpose:** Monitor Switch app health and features

**What it does:**
1. Gets all deployed features
2. Gets all synced agents
3. Gets all workflows
4. Returns complete status

**Parameters:** None

**Returns:** Complete status of Switch app

**Example:**
```python
"What's the current status of Switch app?"
```

---

### 10. `bidirectional_sync`
**Purpose:** Real-time sync between Agent Master ↔ Switch

**Sync types:**
- **push**: Agent Master → Switch
- **pull**: Switch → Agent Master
- **realtime**: Bidirectional Firestore listener

**Parameters:**
- `sync_type`: Type of sync (push, pull, realtime)
- `data`: Data to sync (dict)

**Returns:** Sync result

**Example:**
```python
"Enable realtime sync between Agent Master and Switch"
```

---

## 📤 FILE MANAGEMENT TOOLS (6 tools)
**File:** `switch_app_file_manager.py`

### 11. `upload_file_to_storage`
Upload files to Cloud Storage with metadata

### 12. `process_image_file`
Vision API analysis (labels, text, objects)

### 13. `get_user_files`
List user's files with filters

### 14. `delete_file`
Remove files securely

### 15. `generate_signed_url`
Secure file access URLs (expires after X hours)

### 16. `create_file_collection`
Organize files into albums/collections

---

## 🤖 AGENT BUILDER TOOLS (4 tools)
**File:** `switch_app_agent_builder.py`

### 17. `create_switch_user_agent`
Create personal AI assistant for a user

### 18. `create_switch_customer_service_agent`
Create customer support agent for businesses

### 19. `integrate_notebooklm_with_agent`
Add NotebookLM knowledge base to agent

### 20. `generate_switch_app_chatbot_ui_code`
Generate React Native chatbot UI code

---

## 🎯 COMMON WORKFLOWS

### Workflow 1: Build Complete Switch App
```
User: "Build a complete Switch app for user Sarah with business 'Pet Store'"

Tool Chain:
1. build_switch_app_agent_workflow
   ├─ create_switch_user_agent
   ├─ create_switch_customer_service_agent
   ├─ integrate_notebooklm_with_agent (x2)
   ├─ generate_switch_app_chatbot_ui_code
   └─ Save to Firestore

Result: Complete app with 2 agents, UI code, and NotebookLM
```

### Workflow 2: Upload & Process File
```
User: "Upload this product image and organize it"

Tool Chain:
1. upload_and_process_file_workflow
   ├─ upload_file_to_storage
   ├─ process_image_file (Vision API)
   └─ Suggest collection based on labels

Result: File uploaded, analyzed, collection suggested
```

### Workflow 3: Deploy Agent to Production
```
User: "Deploy my agent to Cloud Run"

Tool Chain:
1. deploy_agent_to_cloud_workflow
   ├─ Verify agent exists
   ├─ CloudExpert: verify_before_deploy
   ├─ CloudExpert: deploy to Cloud Run
   └─ CloudExpert: validate_deployment_success

Result: Agent live at https://agent-service-PROJECT_ID.run.app
```

### Workflow 4: Build Feature from Prompt
```
User: "Build a video uploader with progress bar for Switch"

Tool Chain:
1. create_switch_feature_from_prompt
   ├─ CodeMaster: Generate React component
   ├─ deploy_feature_to_switch
   └─ deploy_to_switch_firebase (optional)

Result: Feature code generated and ready for deployment
```

### Workflow 5: Sync Agent to Switch
```
User: "Add my CS agent as a chatbot in Switch"

Tool Chain:
1. sync_agent_to_switch (integration_type='chatbot')
   ├─ Get agent config
   ├─ generate_switch_app_chatbot_ui_code
   └─ deploy_feature_to_switch

Result: Chatbot component deployed to Switch
```

---

## 🔗 Tool Dependencies

```
intelligent_tool_chain
├─ build_switch_app_agent_workflow
│  ├─ create_switch_user_agent
│  ├─ create_switch_customer_service_agent
│  ├─ integrate_notebooklm_with_agent
│  └─ generate_switch_app_chatbot_ui_code
│
├─ upload_and_process_file_workflow
│  ├─ upload_file_to_storage
│  └─ process_image_file
│
├─ deploy_agent_to_cloud_workflow
│  └─ CloudExpert (sub-agent)
│
└─ create_switch_feature_from_prompt
   ├─ CodeMaster (sub-agent)
   ├─ deploy_feature_to_switch
   └─ deploy_to_switch_firebase
```

---

## 📊 Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Workflow Orchestration** | 4 | Chain tools together automatically |
| **Switch Integration** | 6 | Connect Agent Master ↔ Switch |
| **File Management** | 6 | Upload, process, organize files |
| **Agent Builder** | 4 | Create and configure agents |
| **TOTAL** | **20** | Make 126 tools work together |

---

## 🚀 Quick Start Examples

### Example 1: Natural Language Feature Creation
```
"Build a drag-and-drop file uploader for Switch app"
→ Uses: create_switch_feature_from_prompt
→ Result: Complete React component with Tailwind CSS
```

### Example 2: Complete App Setup
```
"Setup Switch app for user Mike with business 'Coffee Shop'"
→ Uses: build_switch_app_agent_workflow
→ Result: 2 agents, UI code, NotebookLM integrated
```

### Example 3: Smart File Upload
```
"Upload this image and tell me what's in it"
→ Uses: upload_and_process_file_workflow
→ Result: Uploaded + Vision analysis + Collection suggestion
```

---

## 🔧 Configuration

All tools use:
- **Project ID**: `studio-2416451423-f2d96`
- **Firestore**: For tracking and state
- **Cloud Storage**: For file uploads
- **Switch Repo**: `https://github.com/LiveRichCopilot/switch.git`
- **Agent Master Repo**: `https://github.com/LiveRichCopilot/AgentMaster.git`

---

## 📝 Notes

1. **Tool Chaining**: Tools automatically call each other based on workflow logic
2. **Error Handling**: Each workflow tracks status and returns detailed error messages
3. **Firestore Tracking**: All workflows save their progress to Firestore
4. **Sub-Agent Integration**: Workflows can call CodeMaster, CloudExpert, DatabaseExpert
5. **Natural Language**: `intelligent_tool_chain` understands natural language goals

---

**Total Tools in JAi Cortex: 146**
- 126 individual tools
- 20 workflow/integration tools (documented here)

**GitHub:** https://github.com/LiveRichCopilot/AgentMaster.git
