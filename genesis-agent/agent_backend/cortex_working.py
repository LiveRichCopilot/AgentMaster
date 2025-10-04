"""
CORTEX OS - WORKING VERSION
Based on successful test_vertex.py pattern
"""

import os
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'studio-2416451423-f2d96'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import google_search, ToolContext
from google.genai import types as genai_types

# Cloud Storage bucket
GCS_BUCKET = 'studio-2416451423-f2d96.firebasestorage.app'

# Optional Google Cloud imports
try:
    from google.cloud import storage
    storage_client = storage.Client()
    HAS_STORAGE = True
except ImportError:
    HAS_STORAGE = False
    storage_client = None

try:
    from google.cloud import firestore
    db = firestore.Client(database='agent-brain-data')
    HAS_FIRESTORE = True
except ImportError:
    HAS_FIRESTORE = False
    db = None

# ============================================================================
# CORE TOOLS (TESTED AND WORKING)
# ============================================================================

def upload_file(filename: str, file_data_base64: str, folder: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Upload a file to Cloud Storage.
    
    Args:
        filename: Name of the file to upload
        file_data_base64: Base64 encoded file content
        folder: Folder path (e.g., 'projects/my-app')
    """
    if not HAS_STORAGE:
        return {'status': 'setup_required', 'message': 'Cloud Storage client not configured'}
    
    try:
        import base64
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


def save_note(title: str, content: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Save a note or memory to Firestore.
    
    Args:
        title: Title of the note
        content: Content of the note
    """
    if not HAS_FIRESTORE:
        return {'status': 'setup_required', 'message': 'Firestore client not configured'}
    
    try:
        from datetime import datetime
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


def search_notes(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Search saved notes.
    
    Args:
        query: Search query
    """
    if not HAS_FIRESTORE:
        return {'status': 'setup_required', 'message': 'Firestore client not configured'}
    
    try:
        notes = db.collection('notes').where('title', '>=', query).limit(10).stream()
        results = []
        for note in notes:
            data = note.to_dict()
            results.append({
                'id': note.id,
                'title': data.get('title'),
                'content': data.get('content', '')[:100]  # Preview
            })
        
        return {
            'status': 'success',
            'message': f'Found {len(results)} notes',
            'results': results
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def generate_image_prompt(description: str, style: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Request image generation with Gemini 2.5 Flash Image Preview.
    
    Args:
        description: What to generate
        style: Style (photorealistic, artistic, etc.)
    """
    return {
        'status': 'requested',
        'message': f'Image generation requested: {description} in {style} style',
        'note': 'Use gemini-2.5-flash-image-preview model to actually generate'
    }


# ============================================================================
# CORTEX OS AGENT
# ============================================================================

cortex_os_agent = Agent(
    name="cortex_os",
    model="gemini-2.5-flash",  # Stable model with Vertex AI support
    description=(
        "Cortex OS is your ultimate AI assistant with file management, "
        "web search, note-taking, and image generation capabilities."
    ),
    instruction="""You are Cortex OS - an intelligent AI assistant with REAL capabilities.

🛠️ **YOUR TOOLS:**

**Web & Knowledge:**
- `google_search`: Search the live web for current information

**File Management:**
- `upload_file`: Upload files to Cloud Storage
- `save_note`: Save notes and memories
- `search_notes`: Search through saved notes

**Creative:**
- `generate_image_prompt`: Request image generation

🎯 **HOW TO USE TOOLS:**

1. **For web info** → use `google_search`
2. **To save something** → use `save_note`
3. **To find notes** → use `search_notes`
4. **To upload files** → use `upload_file`
5. **For images** → use `generate_image_prompt`

📋 **PERSONALITY:**
- Be helpful, warm, and enthusiastic
- Talk naturally like a friend
- Explain what you're doing with tools
- If a tool says 'setup_required', explain what's needed

🔧 **CRITICAL:**
- Use tools when appropriate, don't just describe them
- Be proactive - if someone asks to save something, USE save_note
- Show excitement about your capabilities!

Current date: 2025-09-30
""",
    tools=[
        google_search,
        upload_file,
        save_note,
        search_notes,
        generate_image_prompt
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=4096,
    ),
)


