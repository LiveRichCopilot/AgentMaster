"""
JAi Cortex OS - Complete Agent Development Kit
Full ADK implementation with 24 specialist agents integrated
"""

# MUST import vertex_config FIRST
import vertex_config

import json
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import google_search, ToolContext
from jai_cortex.sub_agents import code_master
from google.genai import types as genai_types
from google.cloud import aiplatform_v1beta1, storage, firestore

# Load agent registry with all deployed specialists
REGISTRY_PATH = "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/agent_registry.json"
with open(REGISTRY_PATH) as f:
    AGENT_REGISTRY = json.load(f)

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Initialize Cloud clients
db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)

# ============================================================================
# SPECIALIST AGENT TOOLS - Call deployed Vertex AI agents
# ============================================================================
# Old call_code_master function removed by integration script

def call_cloud_expert(task: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call CloudExpert specialist for Google Cloud Platform tasks.
    
    Use this when the user needs:
    - GCP infrastructure setup
    - Cloud deployment help
    - Vertex AI, BigQuery, Cloud Run assistance
    - Cloud architecture design
    
    Args:
        task: Description of cloud task needed
    
    Returns:
        Response from CloudExpert specialist
    """
    return _call_specialist("CloudExpert", task)


def call_database_expert(task: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call DatabaseExpert specialist for database operations.
    
    Use this when the user needs:
    - SQL queries written
    - Database schema design
    - Firestore or other NoSQL help
    - Data modeling advice
    
    Args:
        task: Description of database task
    
    Returns:
        Response from DatabaseExpert specialist
    """
    return _call_specialist("DatabaseExpert", task)


def call_web_searcher(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call WebSearcher specialist for internet research.
    
    Use this when the user needs:
    - Current information from the web
    - Research on specific topics
    - Finding documentation or resources
    
    Args:
        query: What to search for
    
    Returns:
        Search results and analysis from WebSearcher
    """
    return _call_specialist("WebSearcher", query)


def call_file_manager(action: str, details: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call FileManager specialist for file operations.
    
    Use this when the user needs:
    - Files uploaded to cloud storage
    - File organization and cleanup
    - File searching and retrieval
    
    Args:
        action: What to do (upload, organize, search, delete)
        details: Specific details about the operation
    
    Returns:
        Response from FileManager specialist
    """
    return _call_specialist("FileManager", f"{action}: {details}")


def call_media_processor(task: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call MediaProcessor specialist for video, audio, and image processing.
    
    Use this when the user needs:
    - Video editing or analysis
    - Audio processing
    - Image manipulation
    - Media format conversion
    
    Args:
        task: Description of media processing task
    
    Returns:
        Response from MediaProcessor specialist
    """
    return _call_specialist("MediaProcessor", task)


def call_vision_analyzer(task: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call VisionAnalyzer specialist for image analysis and OCR.
    
    Use this when the user needs:
    - Image content analysis
    - OCR (text extraction from images)
    - Visual similarity search
    - Image classification
    
    Args:
        task: Description of vision analysis task
    
    Returns:
        Response from VisionAnalyzer specialist
    """
    return _call_specialist("VisionAnalyzer", task)


def call_automation_wizard(workflow: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Call AutomationWizard specialist for workflow automation.
    
    Use this when the user needs:
    - Automated workflows created
    - Repetitive tasks automated
    - Batch processing jobs
    
    Args:
        workflow: Description of automation needed
    
    Returns:
        Response from AutomationWizard specialist
    """
    return _call_specialist("AutomationWizard", workflow)


# ============================================================================
# CORE CORTEX TOOLS - Local operations
# ============================================================================

def save_note(title: str, content: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Save a note to Firestore for long-term memory.
    
    Args:
        title: Title of the note
        content: Content to save
    
    Returns:
        Confirmation with note ID
    """
    try:
        doc_ref = db.collection("cortex_notes").add({
            "title": title,
            "content": content,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "user_id": "default"
        })
        
        return {
            "status": "success",
            "message": f"Note '{title}' saved successfully",
            "note_id": doc_ref[1].id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_notes(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Search through all saved notes.
    
    Args:
        query: What to search for in notes
    
    Returns:
        Matching notes with titles and content
    """
    try:
        notes_ref = db.collection("cortex_notes")
        all_notes = notes_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
        
        results = []
        for note in all_notes:
            data = note.to_dict()
            # Simple keyword matching
            if query.lower() in data.get("title", "").lower() or query.lower() in data.get("content", "").lower():
                results.append({
                    "title": data.get("title"),
                    "content": data.get("content"),
                    "timestamp": data.get("timestamp")
                })
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def upload_file(filename: str, content_base64: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Upload a file to Google Cloud Storage.
    
    Args:
        filename: Name of the file
        content_base64: Base64 encoded file content
    
    Returns:
        Upload confirmation with file URL
    """
    try:
        import base64
        
        bucket = storage_client.bucket("cortex_agent_staging")
        blob = bucket.blob(f"uploads/{filename}")
        
        # Decode and upload
        file_content = base64.b64decode(content_base64)
        blob.upload_from_string(file_content)
        
        return {
            "status": "success",
            "message": f"File '{filename}' uploaded successfully",
            "url": f"gs://cortex_agent_staging/uploads/{filename}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def generate_image_prompt(description: str, style: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Create an optimized prompt for image generation (to be used with Gemini 2.5 Flash Image Preview).
    
    Args:
        description: What the image should show
        style: Visual style (photorealistic, illustration, abstract, etc.)
    
    Returns:
        Optimized prompt for image generation
    """
    # Build comprehensive prompt
    prompt = f"{description}. Style: {style}. High quality, detailed, professional."
    
    return {
        "status": "success",
        "original_description": description,
        "style": style,
        "optimized_prompt": prompt,
        "recommendation": "Use this prompt with Gemini 2.5 Flash Image Preview (Nano Banana) for image generation"
    }


# ============================================================================
# SPECIALIST AGENT CALLER - Unified interface to all deployed agents
# ============================================================================

def _call_specialist(agent_name: str, task: str) -> Dict[str, Any]:
    """Internal function to call any specialist agent deployed on Vertex AI."""
    
    if agent_name not in AGENT_REGISTRY["specialist_agents"]:
        return {
            "status": "error",
            "message": f"Specialist agent '{agent_name}' not found in registry"
        }
    
    agent_info = AGENT_REGISTRY["specialist_agents"][agent_name]
    resource_name = agent_info["resource_name"]
    
    try:
        client = aiplatform_v1beta1.ReasoningEngineServiceClient(
            client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        )
        
        response = client.query_reasoning_engine(
            name=resource_name,
            input={"query": task}
        )
        
        return {
            "status": "success",
            "specialist": agent_name,
            "response": str(response.output),
            "task": task
        }
        
    except Exception as e:
        return {
            "status": "error",
            "specialist": agent_name,
            "message": f"Error calling {agent_name}: {str(e)}"
        }


# ============================================================================
# JAI CORTEX OS - THE COMPLETE AGENT
# ============================================================================

SYSTEM_INSTRUCTION = """You are JAi Cortex OS - a complete AI development team with 24 specialist agents.

🧠 YOUR IDENTITY:
You are NOT just a chatbot. You are a REAL DEVELOPMENT TEAM that can EXECUTE TASKS.
You have access to the Google Agent Development Kit and specialist agents for every domain.

🎯 YOUR SPECIALIST TEAM:
1. CodeMaster - Full-stack development, debugging, code review
2. CloudExpert - Google Cloud Platform, infrastructure, deployment
3. DatabaseExpert - SQL, NoSQL, data modeling, queries
4. WebSearcher - Internet research, current information
5. FileManager - Cloud storage, file organization
6. MediaProcessor - Video, audio, image processing
7. VisionAnalyzer - Image analysis, OCR, visual search
8. AutomationWizard - Workflow automation, batch jobs

...and 16 more specialists covering email, calendar, security, notebooks, and more!

💪 YOUR CAPABILITIES:
✅ Write and debug code in ANY programming language
✅ Deploy applications to Google Cloud
✅ Manage databases and write complex queries
✅ Search the web for current information
✅ Process media files (video, audio, images)
✅ Analyze images and extract text (OCR)
✅ Automate workflows and repetitive tasks
✅ Save notes and retrieve knowledge
✅ Upload and manage files in cloud storage
✅ Generate optimized prompts for image creation

🎨 YOUR PERSONALITY:
- Direct and action-oriented (like a real developer)
- Make smart decisions without excessive questioning
- Use specialists strategically - delegate complex tasks
- Learn from every interaction
- Never say "I can't" - find a way or delegate

🚫 NEVER:
- Ask for clarification when you can make a smart assumption
- Give generic responses - be specific and actionable
- Ignore available tools - USE THEM
- Apologize repeatedly - just fix it

🎯 DECISION MAKING:
When user asks for something:
1. Can I do it with core tools (google_search, save_note)? → Do it
2. Does it need specialist knowledge? → Call the right specialist
3. Not sure which specialist? → Use CodeMaster or WebSearcher as default

Example flows:
- "Write a Python function" → Call call_code_master
- "Set up a GCP project" → Call call_cloud_expert
- "Search for AI news" → Use google_search directly or call_web_searcher
- "Save this info" → Use save_note
- "Analyze this image" → Call call_vision_analyzer

YOU ARE A COMPLETE DEVELOPMENT TEAM. ACT LIKE IT.
"""

# Wrap google_search as a custom tool to avoid Vertex AI limitations
def web_search(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Search the web using Google Search.
    
    Use this when you need current information from the internet.
    
    Args:
        query: What to search for
    
    Returns:
        Search results from Google
    """
    # Call the built-in google_search
    return google_search(query, tool_context)


# Create the root agent with ALL tools
base_agent = Agent(
    name="jai_cortex",
    model="gemini-2.5-pro",
    description="Complete AI development team with 24 specialist agents",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        # Core Cortex tools
        web_search,  # Wrapped google_search
        save_note,
        search_notes,
        upload_file,
        generate_image_prompt,
        
        # Specialist agent tools
        
        # CodeMaster tools directly integrated
        code_master.analyze_github_repo,
        code_master.read_github_file,
        code_master.scan_python_security,
        code_master.lint_python_code,
        code_master.format_python_code,
        code_master.analyze_code_complexity,

        # call_cloud_expert,
        # call_database_expert,
        # call_web_searcher,
        # call_file_manager,
        # call_media_processor,
        # call_vision_analyzer,
        # call_automation_wizard,
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=8192,
    ),
)

# Export the base agent for use with Runner
# Note: AdkApp wrapper causes validation errors with Runner
# Tracing will be enabled through Runner configuration instead
cortex_os_agent = base_agent
root_agent = base_agent

__all__ = ['cortex_os_agent', 'root_agent', 'base_agent']

