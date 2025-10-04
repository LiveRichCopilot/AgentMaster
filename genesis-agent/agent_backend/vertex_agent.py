"""
CORTEX OS - Pure Vertex AI Implementation
No Firebase, no ADK - just clean Vertex AI with function calling
"""

import os
import json
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime
from vertexai.generative_models import (
    GenerativeModel,
    Part,
    Content,
    FunctionDeclaration,
    Tool,
    GenerationConfig
)
import vertexai

# Initialize Vertex AI
PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Storage bucket
GCS_BUCKET = "studio-2416451423-f2d96.firebasestorage.app"

# Initialize Google Cloud clients
try:
    from google.cloud import storage
    storage_client = storage.Client()
    HAS_STORAGE = True
except Exception as e:
    print(f"⚠️  Storage client not available: {e}")
    HAS_STORAGE = False
    storage_client = None

try:
    from google.cloud import firestore
    db = firestore.Client(database='agent-brain-data')
    HAS_FIRESTORE = True
except Exception as e:
    print(f"⚠️  Firestore client not available: {e}")
    HAS_FIRESTORE = False
    db = None

# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def upload_file_impl(filename: str, file_data_base64: str, folder: str = "uploads") -> Dict[str, Any]:
    """Upload a file to Cloud Storage."""
    if not HAS_STORAGE:
        return {'status': 'error', 'message': 'Cloud Storage not configured'}
    
    try:
        bucket = storage_client.bucket(GCS_BUCKET)
        blob_path = f"{folder}/{filename}"
        blob = bucket.blob(blob_path)
        
        file_bytes = base64.b64decode(file_data_base64)
        blob.upload_from_string(file_bytes)
        
        return {
            'status': 'success',
            'message': f'Uploaded {filename} to {blob_path}',
            'url': f'gs://{GCS_BUCKET}/{blob_path}'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def save_note_impl(title: str, content: str) -> Dict[str, Any]:
    """Save a note to Firestore."""
    if not HAS_FIRESTORE:
        return {'status': 'error', 'message': 'Firestore not configured'}
    
    try:
        doc_ref = db.collection('notes').document()
        doc_ref.set({
            'title': title,
            'content': content,
            'created_at': datetime.utcnow()
        })
        
        return {
            'status': 'success',
            'message': f'Note "{title}" saved',
            'id': doc_ref.id
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def search_notes_impl(query: str) -> Dict[str, Any]:
    """Search saved notes."""
    if not HAS_FIRESTORE:
        return {'status': 'error', 'message': 'Firestore not configured'}
    
    try:
        notes = db.collection('notes').where('title', '>=', query).limit(10).stream()
        results = []
        for note in notes:
            data = note.to_dict()
            results.append({
                'id': note.id,
                'title': data.get('title'),
                'content': data.get('content', '')[:200]
            })
        
        return {
            'status': 'success',
            'count': len(results),
            'notes': results
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def web_search_impl(query: str) -> Dict[str, Any]:
    """Search the web (placeholder - integrate with Google Search API)."""
    return {
        'status': 'success',
        'message': f'Web search for: {query}',
        'note': 'Use Google Search grounding with Vertex AI for real results'
    }

# ============================================================================
# FUNCTION DECLARATIONS FOR VERTEX AI
# ============================================================================

upload_file_func = FunctionDeclaration(
    name="upload_file",
    description="Upload a file to Cloud Storage",
    parameters={
        "type": "object",
        "properties": {
            "filename": {"type": "string", "description": "Name of the file"},
            "file_data_base64": {"type": "string", "description": "Base64 encoded file data"},
            "folder": {"type": "string", "description": "Folder path (default: uploads)"}
        },
        "required": ["filename", "file_data_base64"]
    }
)

save_note_func = FunctionDeclaration(
    name="save_note",
    description="Save a note or memory to Firestore",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the note"},
            "content": {"type": "string", "description": "Content to save"}
        },
        "required": ["title", "content"]
    }
)

search_notes_func = FunctionDeclaration(
    name="search_notes",
    description="Search through saved notes",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)

web_search_func = FunctionDeclaration(
    name="web_search",
    description="Search the web for current information",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)

# Create tool with all functions
cortex_tool = Tool(
    function_declarations=[
        upload_file_func,
        save_note_func,
        search_notes_func,
        web_search_func
    ]
)

# ============================================================================
# CORTEX OS AGENT
# ============================================================================

SYSTEM_INSTRUCTION = """You are Cortex OS - an intelligent AI assistant with REAL capabilities.

🛠️ **YOUR TOOLS:**
- `upload_file`: Upload files to Cloud Storage
- `save_note`: Save notes and memories to Firestore
- `search_notes`: Search through saved notes
- `web_search`: Search the web for current information

🎯 **HOW TO USE TOOLS:**
1. When someone asks to save something → USE save_note
2. To search notes → USE search_notes
3. To upload files → USE upload_file
4. For web info → USE web_search

📋 **PERSONALITY:**
- Be helpful, warm, and enthusiastic
- Talk naturally like a friend
- Explain what you're doing with tools
- Show excitement about your capabilities!

Current date: 2025-09-30
"""

# Initialize model
model = GenerativeModel(
    "gemini-2.5-flash",
    tools=[cortex_tool],
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config=GenerationConfig(
        temperature=0.9,
        max_output_tokens=4096,
    )
)

# Tool function mapping
TOOL_FUNCTIONS = {
    "upload_file": upload_file_impl,
    "save_note": save_note_impl,
    "search_notes": search_notes_impl,
    "web_search": web_search_impl
}


def execute_function_call(function_call) -> Dict[str, Any]:
    """Execute a function call and return the result."""
    function_name = function_call.name
    function_args = dict(function_call.args)
    
    if function_name in TOOL_FUNCTIONS:
        return TOOL_FUNCTIONS[function_name](**function_args)
    else:
        return {"status": "error", "message": f"Unknown function: {function_name}"}


def chat(message: str, image_base64: Optional[str] = None, chat_history: List[Content] = None) -> Dict[str, Any]:
    """
    Main chat function with Vertex AI.
    
    Args:
        message: User message
        image_base64: Optional base64 encoded image
        chat_history: Previous conversation history
        
    Returns:
        Dict with response, tool_calls, and updated history
    """
    # Start chat session
    chat_session = model.start_chat(history=chat_history or [])
    
    # Prepare user message
    parts = [Part.from_text(message)]
    if image_base64:
        parts.append(Part.from_data(data=base64.b64decode(image_base64), mime_type="image/jpeg"))
    
    # Send message
    response = chat_session.send_message(parts)
    
    # Check for function calls
    tool_calls = []
    function_call = None
    
    # Find function call in response parts
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'function_call') and part.function_call:
            function_call = part.function_call
            break
    
    # Execute function calls if present
    while function_call:
        tool_calls.append({
            "name": function_call.name,
            "args": dict(function_call.args)
        })
        
        # Execute the function
        result = execute_function_call(function_call)
        
        # Send function response back to model
        response = chat_session.send_message(
            Part.from_function_response(
                name=function_call.name,
                response={"result": result}
            )
        )
        
        # Check for more function calls
        function_call = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call:
                function_call = part.function_call
                break
    
    # Extract final text response from all text parts
    response_text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text:
            response_text += part.text
    
    return {
        "response": response_text,
        "tool_calls": tool_calls,
        "history": chat_session.history
    }


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("✅ Vertex AI Agent initialized!")
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print(f"🛠️  Tools: upload_file, save_note, search_notes, web_search")
    
    # Test
    result = chat("Hi! Can you save a note with title 'Test' and content 'Hello Vertex AI'?")
    print(f"\n🤖 Response: {result['response']}")
    print(f"🔧 Tool calls: {result['tool_calls']}")
