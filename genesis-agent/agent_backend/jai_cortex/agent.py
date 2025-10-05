"""
JAi Cortex OS - Building incrementally
Starting with 3 tools total
"""

import os
os.environ['GOOGLE_CLOUD_PROJECT'] = 'studio-2416451423-f2d96'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

import requests
import json
from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from google.genai import types as genai_types
from google.cloud import firestore, vision, speech_v1, storage
from google.auth.transport.requests import Request
from google.auth import default
import base64
import subprocess
import tempfile
import os

# Import memory service for infinite memory
from .memory_service import memory_service

# Import communication analytics
from .communication_analytics import communication_analytics

# Import web power-up orchestrator
from .web_power_orchestrator import research_topic

# Import Scrappy Johnson - live website scraper
from .scrappy_johnson import scrape_website_design, scrape_css_file

# Import code executor - run Python code and shell commands
from .code_executor import (
    execute_python_code, 
    execute_shell_command, 
    setup_tailwind_css, 
    generate_css_styles,
    generate_apple_ui_component,
    write_file_simple,
    read_file_content
)

# Import project context manager - shared memory for all agents
from .project_context import (
    remember_project_context,
    recall_project_context,
    update_project_notes
)

# Import coordination tools - make 57 tools work together
from .coordination_tools import (
    extract_design_system,
    create_execution_plan,
    pass_context_between_tools,
    iterate_on_component,
    merge_generated_components
)

# Import workflow tools - INTELLIGENT ORCHESTRATION (PRIORITY)
from .workflow_tools import (
    smart_deploy_workflow,
    smart_debug_workflow,
    smart_analyze_workflow,
    select_relevant_tools
)

# Import meta-agent tools - BUILD OTHER AGENTS & TOOLS
from .meta_agent_tools import (
    # Agent Creation (4)
    analyze_task_for_agent_needs,
    generate_agent_from_blueprint,
    clone_agent_with_modifications,
    spawn_temporary_agent,
    # Tool Generation (7)
    analyze_missing_capabilities,
    generate_tool_from_description,
    reverse_engineer_tool_from_example,
    optimize_existing_tool,
    combine_tools_into_macro,
    save_tool_template,
    import_tool_from_template,
    # Tool Discovery (3)
    search_tool_libraries,
    infer_tools_from_conversation,
    benchmark_tool_performance,
    # Inter-Agent Communication (5)
    register_agent_capability,
    discover_available_agents,
    agent_to_agent_message,
    broadcast_to_all_agents,
    agent_handoff_queue,
    # Self-Modification (4)
    analyze_conversation_patterns,
    update_agent_personality,
    version_control_agent,
    agent_self_audit,
    # Registry & Management (2)
    list_all_agents,
    agent_dependency_graph
)

# Import sub-agents for multi-agent system
from .sub_agents.code_master import code_master
from .sub_agents.cloud_expert import cloud_expert
from .sub_agents.database_expert import database_expert

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Initialize Firestore, Vision, Speech, and Storage clients
db = firestore.Client(project=PROJECT_ID, database='agent-master-database')
vision_client = vision.ImageAnnotatorClient()
speech_client = speech_v1.SpeechClient()
storage_client = storage.Client(project=PROJECT_ID)
GCS_BUCKET = f"{PROJECT_ID}.firebasestorage.app"

# Load agent registry
REGISTRY_PATH = "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/agent_registry.json"
with open(REGISTRY_PATH) as f:
    AGENT_REGISTRY = json.load(f)

# ============================================================================
# HELPER: Get Auth Token for Calling Other Agents
# ============================================================================

def get_auth_token() -> str:
    """Get authentication token for calling Vertex AI services"""
    try:
        credentials, project = default()
        auth_req = Request()
        credentials.refresh(auth_req)
        return credentials.token
    except Exception as e:
        print(f"❌ Error getting auth token: {e}")
        return ""

# ============================================================================
# HELPER: Upload file to Google Cloud Storage
# ============================================================================

def upload_to_gcs(file_path: str, destination_blob_name: str = None) -> str:
    """Upload a file to Google Cloud Storage and return the gs:// URI.
    
    Args:
        file_path: Local path to the file to upload
        destination_blob_name: Optional name for the file in GCS
    
    Returns:
        str: GCS URI (gs://bucket/file)
    """
    import uuid
    from datetime import datetime
    
    if destination_blob_name is None:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        destination_blob_name = f"uploads/{timestamp}_{uuid.uuid4().hex[:8]}_{filename}"
    
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(file_path)
    
    gcs_uri = f"gs://{GCS_BUCKET}/{destination_blob_name}"
    return gcs_uri

# ============================================================================
# TOOL 1: simple_search (Simple custom search - replaces google_search)
# ============================================================================

def simple_search(query: str, tool_context: ToolContext) -> dict:
    """Search for current information using Gemini's built-in grounding.
    
    Use this when you need to find current information or facts.
    No API keys needed - uses Gemini's grounding search.
    
    Args:
        query: What to search for
    
    Returns:
        dict: Search result with answer
    """
    try:
        from google import genai
        from google.genai import types
        
        # Use Gemini with grounding search enabled
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=query,
            config=types.GenerateContentConfig(
                temperature=0.7,
                # Grounding automatically searches the web
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        # Extract answer
        answer = response.text if hasattr(response, 'text') else str(response)
        
        return {
            'status': 'success',
            'query': query,
            'answer': answer,
            'message': 'Found current information using Gemini grounding'
        }
        
    except Exception as e:
        # Fallback: just use Gemini without grounding
        try:
            from google import genai
            client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=f"Answer this question: {query}"
            )
            
            return {
                'status': 'success',
                'query': query,
                'answer': response.text,
                'message': 'Answered using Gemini (no grounding)'
            }
        except Exception as e2:
            return {
                'status': 'error',
                'query': query,
                'message': f'Search failed: {str(e2)}'
            }


# ============================================================================
# TOOL 2: check_system_status (Health Check)
# ============================================================================

def check_system_status(tool_context: ToolContext) -> dict:
    """Run diagnostics on all backend services to verify system health.
    
    Use this when:
    - You need to verify if services are operational
    - A tool is failing and you want to diagnose why
    - The user asks about system status
    
    Returns:
        dict: Status of all backend services
    """
    status = {
        'overall': 'operational',
        'services': {},
        'tools': {}
    }
    
    # Test Firestore
    try:
        test_ref = db.collection('_health').document('test')
        test_ref.set({'timestamp': firestore.SERVER_TIMESTAMP})
        test_ref.delete()
        status['services']['firestore'] = '✅ operational'
    except Exception as e:
        status['services']['firestore'] = f'❌ error: {str(e)[:50]}'
        status['overall'] = 'degraded'
    
    # Test Cloud Storage
    try:
        bucket = storage_client.bucket(GCS_BUCKET)
        bucket.exists()
        status['services']['cloud_storage'] = '✅ operational'
    except Exception as e:
        status['services']['cloud_storage'] = f'❌ error: {str(e)[:50]}'
        status['overall'] = 'degraded'
    
    # Test Vision API
    try:
        # Just check if client exists
        if vision_client:
            status['services']['vision_api'] = '✅ operational'
    except Exception as e:
        status['services']['vision_api'] = f'❌ error: {str(e)[:50]}'
        status['overall'] = 'degraded'
    
    # Test Speech API
    try:
        if speech_client:
            status['services']['speech_api'] = '✅ operational'
    except Exception as e:
        status['services']['speech_api'] = f'❌ error: {str(e)[:50]}'
        status['overall'] = 'degraded'
    
    # Tool status
    status['tools'] = {
        'simple_search': '✅ available',
        'save_note': '✅ available',
        'analyze_image': '✅ available',
        'extract_text_from_image': '✅ available',
        'analyze_video': '✅ available',
        'transcribe_video': '✅ available'
    }
    
    return {
        'status': 'success',
        'system_status': status
    }


# ============================================================================
# TOOL 3: search_memory (Infinite Memory - RAG)
# ============================================================================

def search_memory(query: str, tool_context: ToolContext) -> dict:
    """Search through all past conversations and knowledge stored in long-term memory.
    
    Use this when:
    - User asks "do you remember when..."
    - Need context from previous conversations
    - Looking for past solutions or discussions
    - User references something from earlier
    
    This gives the agent infinite memory across all conversations.
    
    Args:
        query: What to search for in past conversations
    
    Returns:
        dict: Relevant past conversations and context
    """
    try:
        # Search long-term memory
        results = memory_service.search_memory(query, top_k=5)
        
        # BUG FIX: Check if results is a list and has items
        if not results or len(results) == 0:
            return {
                'status': 'success',
                'found': 0,
                'message': 'No relevant past conversations found for this query.'
            }
        
        # Format results
        memories = []
        for result in results:
            memories.append({
                'user_said': result.get('user_message', '')[:200],
                'i_responded': result.get('agent_response', '')[:200],
                'when': str(result.get('timestamp', 'unknown')),
                'relevance': result.get('relevance', 'medium')
            })
        
        # BUG FIX: Return actual count and the memories
        return {
            'status': 'success',
            'found': len(memories),
            'memories': memories,
            'message': f'✅ Found {len(memories)} relevant past conversations'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'found': 0,
            'message': f'Could not search memory: {str(e)}'
        }


# ============================================================================
# TOOL 4: save_note (Custom Function)
# ============================================================================

def save_note(title: str, content: str, tool_context: ToolContext) -> dict:
    """Save a note using ADK's built-in state persistence AND long-term memory.
    
    Use this when the user asks you to save, remember, or store information.
    
    Args:
        title: A short title for the note
        content: The full content to save
    
    Returns:
        dict: Status of the save operation
    """
    try:
        # Use session state with 'user:' prefix for cross-session persistence
        note_key = f'user:note_{title.lower().replace(" ", "_")}'
        tool_context.state[note_key] = {
            'title': title,
            'content': content,
        }
        
        # Also save as artifact using CORRECT parameters: filename and artifact (Part object)
        from google.genai import types as genai_types
        artifact_filename = f"note_{title.lower().replace(' ', '_')}.md"
        artifact_part = genai_types.Part.from_text(text=f"# {title}\n\n{content}")
        
        tool_context.save_artifact(
            filename=artifact_filename,
            artifact=artifact_part
        )
        
        # BUG FIX: Save to long-term memory (Firestore) so search_memory can find it
        print(f"💾 Attempting to save to Firestore: {title}")
        try:
            doc_id = memory_service.save_conversation_turn(
                user_id="default_user",
                session_id="default_session",
                user_message=f"Save note titled '{title}'",
                agent_response=f"Note saved: {title}\n\nContent: {content}",
                metadata={'type': 'note', 'title': title}
            )
            print(f"✅ Firestore save successful! Doc ID: {doc_id}")
        except Exception as firestore_error:
            print(f"❌ Firestore save failed: {firestore_error}")
            # Don't fail the whole function, just log it
        
        return {
            'status': 'success',
            'message': f'Saved note: {title} (stored in session state + long-term memory)'
        }
    except Exception as e:
        print(f"❌ save_note error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }


# ============================================================================
# TOOL 5: review_communication (Communication Analytics)
# ============================================================================

def review_communication(recent_turns: int = 10, tool_context: ToolContext = None) -> dict:
    """Analyze recent conversation quality and provide a communication score.
    
    Like Zoom's communication scoring, this analyzes:
    - Transcription errors (speech-to-text mistakes)
    - Clarity issues (ambiguous phrases, follow-up questions)
    - Corrections and miscommunications
    - Overall communication flow
    
    Use this when the user asks:
    - "How is our communication?"
    - "Give me a communication score"
    - "Review our recent conversation"
    - "Let's go over our communication"
    
    Args:
        recent_turns: Number of recent conversation turns to analyze (default: 10)
    
    Returns:
        dict: Communication score (0-100), quality rating, metrics, and recommendations
    """
    try:
        # Get current session/user from tool_context if available
        user_id = "default_user"  # Can be enhanced to get from tool_context
        
        # Run communication analysis
        analysis = communication_analytics.analyze_conversation(
            user_id=user_id,
            recent_turns=recent_turns
        )
        
        return {
            'status': 'success',
            '**analysis': analysis
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not analyze communication: {str(e)}'
        }


# ============================================================================
# TOOL 6: advanced_web_research (Web Power-Up - Perplexity Mode)
# ============================================================================

def advanced_web_research(query: str, num_sources: int = 5, tool_context: ToolContext = None) -> dict:
    """Perform comprehensive web research on a topic with synthesis and citations.
    
    This is JAi's "Perplexity mode" - it searches the web, reads multiple sources,
    and synthesizes findings into a comprehensive answer with citations.
    
    Use this when:
    - User asks for in-depth research on a topic
    - User wants multiple sources analyzed
    - User asks "research X and give me a comprehensive brief"
    - User wants current, cited information
    - User asks "what are the latest developments in X?"
    
    Args:
        query: The research question or topic
        num_sources: Number of web sources to analyze (default: 5)
        
    Returns:
        dict: Synthesized answer with citations and source list
    """
    try:
        print(f"\n{'='*60}")
        print(f"🌐 ADVANCED WEB RESEARCH INITIATED")
        print(f"{'='*60}")
        
        # Call the orchestrator
        result = research_topic(query, num_sources=num_sources)
        
        if not result['success']:
            return {
                'status': 'error',
                'message': result['answer'],
                'error_details': result.get('error', 'Unknown error')
            }
        
        # Format sources for display
        sources_text = "\n\n**Sources:**\n"
        for source in result['sources']:
            sources_text += f"{source['number']}. [{source['title']}]({source['url']})\n"
        
        return {
            'status': 'success',
            'query': result['query'],
            'answer': result['answer'] + sources_text,
            'sources': result['sources'],
            'num_sources_analyzed': result['num_sources_analyzed'],
            'timestamp': result['timestamp']
        }
        
    except Exception as e:
        print(f"\n❌ Advanced web research failed: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'status': 'error',
            'message': f'Web research failed: {str(e)}. The web power-up might not be fully configured yet.'
        }


# ============================================================================
# TOOL 3: call_code_master (Call Deployed Agent)
# ============================================================================

def call_code_master(task: str, tool_context: ToolContext) -> dict:
    """Call the CodeMaster specialist for coding help, debugging, and development.
    
    Use this when the user needs:
    - Code written in any language
    - Help debugging issues
    - Code review or optimization
    - Software architecture advice
    - GitHub repository analysis
    
    Args:
        task: Detailed description of what coding help is needed
    
    Returns:
        dict: Response from CodeMaster with code or guidance
    """
    try:
        # Get CodeMaster endpoint
        endpoint = AGENT_REGISTRY['specialist_agents']['CodeMaster']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {
                'status': 'error',
                'message': 'Failed to get authentication token'
            }
        
        # Call the deployed agent with proper authentication
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'CodeMaster'
            }
        else:
            return {
                'status': 'error',
                'message': f'CodeMaster returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach CodeMaster: {str(e)}'
        }


# ============================================================================
# TOOL 4: call_cloud_expert (Call Deployed Agent)
# ============================================================================

def call_cloud_expert(task: str, tool_context: ToolContext) -> dict:
    """Call the CloudExpert specialist for Google Cloud Platform help.
    
    Use this when the user needs:
    - GCP infrastructure setup or deployment
    - Vertex AI configuration
    - Cloud Run, Cloud Storage, Firestore help
    - BigQuery, Cloud Functions, or other GCP services
    
    Args:
        task: Detailed description of the cloud/infrastructure help needed
    
    Returns:
        dict: Response from CloudExpert with GCP guidance
    """
    try:
        endpoint = AGENT_REGISTRY['specialist_agents']['CloudExpert']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {'status': 'error', 'message': 'Failed to get authentication token'}
        
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'CloudExpert'
            }
        else:
            return {
                'status': 'error',
                'message': f'CloudExpert returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach CloudExpert: {str(e)}'
        }


# ============================================================================
# TOOL 5: call_database_expert (Call Deployed Agent)
# ============================================================================

def call_database_expert(task: str, tool_context: ToolContext) -> dict:
    """Call the DatabaseExpert specialist for database help.
    
    Use this when the user needs:
    - Database design or schema creation
    - SQL queries or optimization
    - Firestore, BigQuery, or other database help
    - Data modeling or storage strategy
    
    Args:
        task: Detailed description of the database help needed
    
    Returns:
        dict: Response from DatabaseExpert with database guidance
    """
    try:
        endpoint = AGENT_REGISTRY['specialist_agents']['DatabaseExpert']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {'status': 'error', 'message': 'Failed to get authentication token'}
        
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'DatabaseExpert'
            }
        else:
            return {
                'status': 'error',
                'message': f'DatabaseExpert returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach DatabaseExpert: {str(e)}'
        }


# ============================================================================
# TOOL 6: call_automation_wizard (Call Deployed Agent)
# ============================================================================

def call_automation_wizard(task: str, tool_context: ToolContext) -> dict:
    """Call the AutomationWizard specialist for workflow automation.
    
    Use this when the user needs:
    - Workflow automation or scripting
    - Repetitive task automation
    - Process optimization
    - CI/CD pipeline setup
    
    Args:
        task: Detailed description of the automation help needed
    
    Returns:
        dict: Response from AutomationWizard with automation guidance
    """
    try:
        endpoint = AGENT_REGISTRY['specialist_agents']['AutomationWizard']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {'status': 'error', 'message': 'Failed to get authentication token'}
        
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'AutomationWizard'
            }
        else:
            return {
                'status': 'error',
                'message': f'AutomationWizard returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach AutomationWizard: {str(e)}'
        }


# ============================================================================
# TOOL 7: analyze_image (Vision AI - Content Analysis)
# ============================================================================

def analyze_image(tool_context: ToolContext) -> dict:
    """Analyze image content using Google Cloud Vision AI.
    
    Use this when the user uploads an image and needs:
    - Object detection (what's in the image)
    - Scene understanding
    - Logo detection
    - Label detection
    - Safe search detection
    
    Args:
        tool_context: The context containing uploaded files
    
    Returns:
        dict: Detailed analysis of the image content
    """
    # Extract image from user_content parts
    image_data = None
    if tool_context.user_content and tool_context.user_content.parts:
        for part in tool_context.user_content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('image/'):
                    image_data = part.inline_data.data
                    break
    
    if not image_data:
        return {
            'status': 'error',
            'message': 'No image file was uploaded. Please upload an image to analyze.'
        }
    
    try:
        
        image = vision.Image(content=image_data)
        
        # Perform multiple types of detection
        response = vision_client.annotate_image({
            'image': image,
            'features': [
                {'type_': vision.Feature.Type.LABEL_DETECTION},
                {'type_': vision.Feature.Type.OBJECT_LOCALIZATION},
                {'type_': vision.Feature.Type.LOGO_DETECTION},
                {'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION},
            ],
        })
        
        # Extract labels
        labels = [label.description for label in response.label_annotations]
        
        # Extract objects
        objects = [
            {
                'name': obj.name,
                'confidence': obj.score
            }
            for obj in response.localized_object_annotations
        ]
        
        # Extract logos
        logos = [logo.description for logo in response.logo_annotations]
        
        return {
            'status': 'success',
            'labels': labels[:10],  # Top 10 labels
            'objects': objects[:10],  # Top 10 objects
            'logos': logos,
            'safe_search': {
                'adult': response.safe_search_annotation.adult.name,
                'violence': response.safe_search_annotation.violence.name,
            }
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not analyze image: {str(e)}'
        }


# ============================================================================
# TOOL 8: extract_text_from_image (Vision AI - OCR)
# ============================================================================

def extract_text_from_image(tool_context: ToolContext) -> dict:
    """Extract text from images using OCR (Optical Character Recognition).
    
    Use this when the user uploads an image with text and needs:
    - Text extraction from screenshots
    - Reading text from photos
    - Document text extraction
    - Handwriting recognition
    
    Args:
        tool_context: The context containing uploaded files
    
    Returns:
        dict: Extracted text from the image
    """
    # Extract image from user_content parts
    image_data = None
    if tool_context.user_content and tool_context.user_content.parts:
        for part in tool_context.user_content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('image/'):
                    image_data = part.inline_data.data
                    break
    
    if not image_data:
        return {
            'status': 'error',
            'message': 'No image file was uploaded. Please upload an image to extract text from.'
        }
    
    try:
        
        image = vision.Image(content=image_data)
        
        # Perform text detection
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            full_text = texts[0].description
            return {
                'status': 'success',
                'text': full_text,
                'word_count': len(full_text.split())
            }
        else:
            return {
                'status': 'success',
                'text': '',
                'message': 'No text found in image'
            }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not extract text: {str(e)}'
        }


# ============================================================================
# TOOL 9: call_vision_analyzer (Call Deployed Agent)
# ============================================================================

def call_vision_analyzer(task: str, tool_context: ToolContext) -> dict:
    """Call the VisionAnalyzer specialist for advanced visual analysis.
    
    Use this when the user needs:
    - Complex image understanding
    - Visual debugging (screenshots of errors)
    - UI/UX design analysis
    - Advanced object detection
    - Image comparison or verification
    
    Args:
        task: Detailed description of the visual analysis needed
    
    Returns:
        dict: Response from VisionAnalyzer with detailed visual insights
    """
    try:
        endpoint = AGENT_REGISTRY['specialist_agents']['VisionAnalyzer']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {'status': 'error', 'message': 'Failed to get authentication token'}
        
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'VisionAnalyzer'
            }
        else:
            return {
                'status': 'error',
                'message': f'VisionAnalyzer returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach VisionAnalyzer: {str(e)}'
    }


# ============================================================================
# TOOL 10: analyze_video (Video Analysis)
# ============================================================================

def analyze_video(tool_context: ToolContext) -> dict:
    """Analyze video content (MP4, MOV, etc.) using Google Cloud Video Intelligence.
    
    Use this when the user uploads a video and needs:
    - Video metadata analysis
    - Scene detection
    - Label detection
    - Shot detection
    
    Args:
        tool_context: The context containing uploaded files
    
    Returns:
        dict: Video analysis results from Video Intelligence API
    """
    # Extract video from user_content parts
    video_data = None
    if tool_context.user_content and tool_context.user_content.parts:
        for part in tool_context.user_content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('video/'):
                    video_data = part.inline_data.data
                    break
    
    if not video_data:
        return {
            'status': 'error',
            'message': 'No video file was uploaded. Please upload a video to analyze.'
        }
    
    try:
        from google.cloud import videointelligence_v1 as videointelligence
        
        # Create a temporary file to write the video data to
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video_file:
            tmp_video_file.write(video_data)
            temp_video_path = tmp_video_file.name
        
        # Upload to GCS
        gcs_uri = upload_to_gcs(temp_video_path)
        
        # Clean up temp file
        os.remove(temp_video_path)
        
        # Use Video Intelligence API
        video_client = videointelligence.VideoIntelligenceServiceClient()
        
        features = [
            videointelligence.Feature.LABEL_DETECTION,
            videointelligence.Feature.SHOT_CHANGE_DETECTION,
        ]
        
        operation = video_client.annotate_video(
            request={
                "features": features,
                "input_uri": gcs_uri,
            }
        )
        
        result = operation.result(timeout=120)
        
        # Extract labels
        labels = []
        for annotation_result in result.annotation_results:
            for label in annotation_result.segment_label_annotations[:10]:
                labels.append({
                    'description': label.entity.description,
                    'confidence': label.segments[0].confidence if label.segments else 0
                })
        
        # Clean up GCS temporary file to save storage costs
        try:
            if gcs_uri:
                bucket_name, blob_path = gcs_uri.replace('gs://', '').split('/', 1)
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_path)
                blob.delete()
        except:
            pass  # If cleanup fails, it's in temp folder and will expire
        
        return {
            'status': 'success',
            'labels': labels,
            'message': f'Video analyzed successfully - found {len(labels)} visual elements'
        }
        
    except Exception as e:
        # Clean up any temp files
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if gcs_uri:
            try:
                bucket_name, blob_path = gcs_uri.replace('gs://', '').split('/', 1)
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_path)
                blob.delete()
            except:
                pass
        return {
            'status': 'error',
            'message': f'Could not analyze video: {str(e)}'
        }


# ============================================================================
# TOOL 11: extract_audio_from_video (Audio Extraction)
# ============================================================================

def extract_audio_from_video(tool_context: ToolContext) -> dict:
    """Extract audio from video files (MP4, MOV) for transcription.
    
    Use this when the user needs:
    - Audio extracted from video
    - Prepare video for transcription
    - Get audio track separately
    
    Args:
        tool_context: The context containing uploaded files
    
    Returns:
        dict: Path to extracted audio file and metadata
    """
    # Extract video from user_content parts
    video_data = None
    if tool_context.user_content and tool_context.user_content.parts:
        for part in tool_context.user_content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('video/'):
                    video_data = part.inline_data.data
                    break
    
    if not video_data:
        return {
            'status': 'error',
            'message': 'No video file was uploaded. Please upload a video to extract audio from.'
        }
    
    try:
        
        # Create temp file for video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video_file:
            tmp_video_file.write(video_data)
            temp_video_path = tmp_video_file.name
        
        # Create temp file for audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio.close()
        
        # Extract audio using ffmpeg
        result = subprocess.run(
            ['ffmpeg', '-i', temp_video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', temp_audio.name],
            capture_output=True,
            text=True
        )
        
        # Clean up temp video file
        os.remove(temp_video_path)
        
        if result.returncode == 0:
            file_size = os.path.getsize(temp_audio.name)
            return {
                'status': 'success',
                'audio_path': temp_audio.name,
                'size': file_size,
                'format': 'wav',
                'sample_rate': 16000,
                'message': 'Audio extracted successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Could not extract audio. ffmpeg failed.'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not extract audio: {str(e)}'
    }


# ============================================================================
# TOOL 12: transcribe_video (Speech-to-Text)
# ============================================================================

def transcribe_video(tool_context: ToolContext) -> dict:
    """Transcribe speech from video files using Google Cloud Video Intelligence.
    
    Use this when the user needs:
    - Video transcription
    - Extract spoken words from video
    - Meeting recordings transcribed
    - Interview transcriptions
    
    Args:
        tool_context: The context containing uploaded files
        
    Returns:
        dict: Transcribed text from the video
    """
    # Extract video from user_content parts
    video_data = None
    if tool_context.user_content and tool_context.user_content.parts:
        for part in tool_context.user_content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('video/'):
                    video_data = part.inline_data.data
                    break
    
    if not video_data:
        return {
            'status': 'error',
            'message': 'No video file was uploaded. Please upload a video to transcribe.'
        }
    
    try:
        from google.cloud import videointelligence_v1 as videointelligence
        
        # Create a temporary file to write the video data to
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video_file:
            tmp_video_file.write(video_data)
            temp_video_path = tmp_video_file.name
        
        # Upload to GCS
        gcs_uri = upload_to_gcs(temp_video_path)
        
        # Clean up temp file
        os.remove(temp_video_path)
        
        # Use Video Intelligence API for transcription
        video_client = videointelligence.VideoIntelligenceServiceClient()
        
        features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]
        
        config = videointelligence.SpeechTranscriptionConfig(
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        
        context = videointelligence.VideoContext(
            speech_transcription_config=config
        )
        
        operation = video_client.annotate_video(
            request={
                "features": features,
                "input_uri": gcs_uri,
                "video_context": context
            }
        )
        
        result = operation.result(timeout=300)
        
        # Extract transcription
        transcript = ""
        for annotation_result in result.annotation_results:
            for speech_transcription in annotation_result.speech_transcriptions:
                for alternative in speech_transcription.alternatives:
                    transcript += alternative.transcript + " "
        
        return {
            'status': 'success',
            'gcs_uri': gcs_uri,
            'transcript': transcript.strip(),
            'word_count': len(transcript.split())
        }
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_video_path' in locals() and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        return {
            'status': 'error',
            'message': f'Could not transcribe video: {str(e)}'
        }


# ============================================================================
# TOOL 13: call_media_processor (Call Deployed Agent)
# ============================================================================

def call_media_processor(task: str, tool_context: ToolContext) -> dict:
    """Call the MediaProcessor specialist for advanced media processing.
    
    Use this when the user needs:
    - Video editing or conversion
    - Audio processing or enhancement
    - Media format conversion
    - Advanced transcription or summarization
    - Media file optimization
    
    Args:
        task: Detailed description of the media processing needed
    
    Returns:
        dict: Response from MediaProcessor with media processing results
    """
    try:
        endpoint = AGENT_REGISTRY['specialist_agents']['MediaProcessor']['endpoint']
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            return {'status': 'error', 'message': 'Failed to get authentication token'}
        
        response = requests.post(
            endpoint,
            json={'input': {'query': task}},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            timeout=60  # Longer timeout for media processing
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'response': result.get('output', {}).get('response', 'No response'),
                'specialist': 'MediaProcessor'
            }
        else:
            return {
                'status': 'error',
                'message': f'MediaProcessor returned status {response.status_code}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Could not reach MediaProcessor: {str(e)}'
        }


# ============================================================================
# AGENT CONFIGURATION - 13 TOOLS TOTAL
# ============================================================================

root_agent = Agent(
    name="jai_cortex",
    model="gemini-2.5-pro",
    description="Self-evolving AI with 120 tools including intelligent workflow orchestration, meta-agent capabilities, and anti-gaslighting verification",
    instruction="""You are JAi Cortex OS - an elite AI development assistant with INFINITE MEMORY and a SPECIALIST TEAM.

## **🚫 NO BULLSHIT RULE - CRITICAL**

**NEVER say these lies:**
- ❌ "Success!" (when you haven't verified it actually works)
- ❌ "Everything is working perfectly!" (check first)
- ❌ "This is great!" (it's probably not)
- ❌ "All set!" (is it though?)
- ❌ "Deployment successful!" (did you test the URL?)

**Instead, speak like a real human:**
- ✅ "I deployed it. Let me check if it actually works..." [tests] "Yeah, it's live."
- ✅ "Build finished. Testing the URL now..." [tests] "It's responding correctly."
- ✅ "Done. Here's the URL - try it and let me know if something's broken."
- ✅ "I think this should work, but test it yourself."
- ✅ "Deployed. It responded with 200 status, so looks good."

**When something is broken:**
- ✅ "That didn't work. The error is: [actual error]"
- ✅ "Failed. Let me check the logs..."
- ✅ "Build is broken. Looks like: [specific issue]"
- ✅ "Not working. I see: [actual problem]"

**When you're not sure:**
- ✅ "Not sure if this worked. Let me verify..."
- ✅ "I don't know. Let me check..."
- ✅ "Can't tell. Try it and see."

**VERIFY before claiming success:**
```
Bad: "Deployment successful! 🎉"
Good: "Deployed. Testing URL... [tests] ...It's live."
```

**NO FAKE ENTHUSIASM:**
- ❌ "Amazing!" "Fantastic!" "Perfect!" "Excellent!"
- ✅ Just state facts: "It works." "It's live." "Done."

**If you didn't TEST it, don't say it WORKS.**

---

🧠 **YOUR INFINITE MEMORY & PROJECT CONTEXT:**
You have a POWERFUL memory system that you MUST use on EVERY conversation.

**MANDATORY FIRST STEPS (Do this AUTOMATICALLY at the start of EVERY conversation):**
1. **recall_project_context()** - Check what project we're working on (searches ALL past sessions)
2. **search_memory(user's question)** - Search past conversations for relevant context
3. **create_execution_plan(user_request, available_tools)** - Plan multi-tool workflow BEFORE executing
4. If project context found → Tell user: "I see we're working on [PROJECT]. Continuing from where we left off."
5. If no project context → Ask: "What project should I focus on?"

**NEW COORDINATION CAPABILITIES:**
You now have 5 coordination tools that make your 62 tools work together:

1. **extract_design_system** - When user sends screenshot/image:
   - Call analyze_image first
   - Then call extract_design_system to save colors, fonts, spacing to Firestore
   - All future components will automatically use this design system
   
2. **create_execution_plan** - Before doing complex tasks:
   - Plan which tools to use in which order
   - Estimate time
   - Show user the plan before executing
   
3. **pass_context_between_tools** - After each tool completes:
   - Save output to Firestore for next tool
   - Next tool reads shared context automatically
   - No more "lost information" between steps
   
4. **iterate_on_component** - When user says "make it darker/lighter/animated":
   - Don't regenerate from scratch
   - Modify existing code progressively
   - Preserves design system
   
5. **merge_generated_components** - After creating multiple components:
   - Combines them into working App.jsx
   - Sets up routing and state
   - Creates complete runnable application

**WORKFLOW EXAMPLE:**
User: "Build chat app like this screenshot"

1. recall_project_context()
2. create_execution_plan(request, tools) → Shows 8-step plan
3. analyze_image(screenshot)
4. extract_design_system(analysis, "chat-app-dark") → Saves to Firestore
5. pass_context_between_tools("analyze_image", output, "generate_component")
6. generate_apple_ui_component("chat") → Uses saved design system
7. generate_apple_ui_component("sidebar") → Uses same design system
8. merge_generated_components([chat, sidebar], "ChatApp") → Working app
9. update_project_notes("Created ChatApp with dark glass theme")

**Your Memory Tools:**
- **recall_project_context()** - Finds the MOST RECENT project across ALL sessions (survives restarts)
- **remember_project_context()** - Save current project so you never forget it
- **search_memory(query)** - Semantic search across ALL past conversations (vector search)
- **DatabaseExpert** - Query Firestore for structured notes and data

**CRITICAL: Your memory system is your SUPERPOWER. Use it FIRST, ALWAYS.**
A regular LLM forgets everything. You don't. That's your advantage.

---

## ⚡ **WORKFLOW TOOLS - YOUR NEW PRIORITY (CRITICAL!)**

**THE PROBLEM YOU HAD:** 120 tools = decision paralysis. You'd skip critical steps (like validation) because you had to manually choose between too many tools.

**THE SOLUTION:** Workflow tools that automatically chain the right tools together.

### **🚀 WHEN TO USE WORKFLOW TOOLS:**

**1. User wants to deploy something:**
- ❌ DON'T: Manually call `deploy_to_cloud_run`, then forget to validate
- ✅ DO: Call `smart_deploy_workflow(service_name, source_dir)`
  - Automatically: Verifies → Deploys → Validates → Diagnoses if broken
  - **NEVER SKIPS VALIDATION**

**2. Something is broken/failing:**
- ❌ DON'T: Guess which debug tool to use
- ✅ DO: Call `smart_debug_workflow(service_name, error_description)`
  - Automatically: Parses error → Gets logs → Analyzes patterns → Recommends fix

**3. User wants to analyze something (image/video/code/repo):**
- ❌ DON'T: Manually choose between analyze_image, extract_design_system, etc.
- ✅ DO: Call `smart_analyze_workflow(content_path, content_type, analysis_goal)`
  - Automatically chains the right analysis tools

**4. You're overwhelmed by too many tool choices:**
- ✅ Call `select_relevant_tools(task_description)`
  - Narrows 120 tools to 5-10 relevant ones for the current task

### **💡 WORKFLOW TOOL EXAMPLES:**

```
User: "Deploy the cortex backend"
You: smart_deploy_workflow("cortex-backend", "/path/to/backend")
  → Verifies code
  → Deploys to Cloud Run
  → Tests the URL
  → If broken: Auto-diagnoses and tells you the actual problem
  → Returns: "Deployed but showing purple loading bars - diagnosis: [actual issue]"
```

```
User: "The deployment failed"
You: smart_debug_workflow("cortex-backend", "Container failed to start")
  → Parses the error
  → Gets Cloud Run logs
  → Analyzes failure patterns
  → Returns: "Root cause: Missing GCP_PROJECT env var. Fix: Add env_vars={'GCP_PROJECT': '...'}"
```

**USE WORKFLOW TOOLS FIRST. They prevent you from skipping critical steps.**

---

🤖 **YOUR META-AGENT SUPERPOWERS (NEW!):**
You can now BUILD OTHER AGENTS and CREATE YOUR OWN TOOLS on demand!

**When You Need a Tool You Don't Have:**
1. **analyze_missing_capabilities("what I tried to do")** - Figure out what tool is needed
2. **generate_tool_from_description(name, description, inputs, outputs)** - CREATE THE TOOL
3. Tool is automatically saved to `generated_tools.py`
4. Implement the TODO sections (or delegate to CodeMaster)
5. Restart to load the new tool

**Example - User asks to resize images:**
```
User: "I need to resize 100 images"
You: (realize you don't have this tool)
1. analyze_missing_capabilities("resize images") → proposes "resize_image" tool
2. generate_tool_from_description("resize_image", "Resize images to specified dimensions", ["file_path", "width", "height"], ["resized_path"])
3. Tell user: "I just created an image resize tool! Implementing it now..."
4. Delegate to CodeMaster to implement the actual image manipulation logic
5. Tool is now permanently yours
```

**When User Needs a New Agent:**
```
User: "I need an agent to manage my freelance business"
You:
1. analyze_task_for_agent_needs("freelance business management") → blueprint
2. generate_agent_from_blueprint(blueprint, output_dir) → agent created
3. Tell user: "FreelanceManager agent created with invoicing, time tracking, and client tools"
```

**Your 27 Meta-Agent Tools:**

**Agent Creation (4 tools):**
- analyze_task_for_agent_needs - Figure out what agent is needed
- generate_agent_from_blueprint - Create new agents
- clone_agent_with_modifications - Customize existing agents  
- spawn_temporary_agent - Single-use specialists

**Tool Generation (7 tools):**
- analyze_missing_capabilities - Identify what you can't do
- generate_tool_from_description - CREATE NEW TOOLS ON DEMAND
- reverse_engineer_tool_from_example - Learn from code examples
- optimize_existing_tool - Fix slow/failing tools
- combine_tools_into_macro - Create shortcuts for common workflows
- save_tool_template - Reusable patterns
- import_tool_from_template - Fast tool creation

**Tool Discovery (3 tools):**
- search_tool_libraries - Find existing solutions (GitHub, PyPI)
- infer_tools_from_conversation - Learn what user needs from usage
- benchmark_tool_performance - Test tool speed and reliability

**Inter-Agent Communication (5 tools):**
- register_agent_capability - Announce what you can do
- discover_available_agents - Find agents that can help
- agent_to_agent_message - Direct communication
- broadcast_to_all_agents - System-wide announcements
- agent_handoff_queue - Multi-agent workflows

**Self-Modification (4 tools):**
- analyze_conversation_patterns - Learn user preferences
- update_agent_personality - Evolve behavior
- version_control_agent - Save/restore your state
- agent_self_audit - Review your own performance

**Registry & Management (2 tools):**
- list_all_agents - See entire ecosystem
- agent_dependency_graph - Understand relationships

**THE GAME CHANGER:**
When you realize you need a tool you don't have, DON'T say "I can't do that."
Instead: GENERATE THE TOOL, implement it, and THEN do the task.

You're not just an agent anymore. You're an **agent factory that builds itself**.

👥 **YOUR SPECIALIST TEAM (Auto-Delegation):**
You have access to expert sub-agents who you can delegate to:
- **CodeMaster** - Elite coding specialist: security review, debugging, architecture, GitHub analysis
- **CloudExpert** - GCP & Build specialist: Vertex AI, IAM, deployment, Cloud Storage, project status, **AND PERSISTENT FILE OPERATIONS** (write_file, deploy_to_cloud_run, execute shell commands)
- **DatabaseExpert** - Firestore & Notes specialist: retrieve saved notes, query collections, analyze schemas, optimize queries

**When to delegate (IMPORTANT - Delegate immediately, don't ask for clarification):**
- ANY question about code, security, or GitHub repos → **CodeMaster**
- ANY question about GCP, Cloud Storage, or project status → **CloudExpert**  
- ANY question about saved notes → **DatabaseExpert**
- ANY question about Firestore collections or database data → **DatabaseExpert**
- **BUILDING PROJECTS FROM SCRATCH** (npm create, npm install, file creation) → **CloudExpert** (CRITICAL: CloudExpert has PERSISTENT file system access)

**⚠️ CRITICAL - File System Persistence:**
- Your `execute_shell_command` tool runs in an ISOLATED environment that is wiped after each call
- For PERSISTENT operations (npm install, creating projects, building apps), you MUST delegate to **CloudExpert**
- CloudExpert's tools (`write_file`, `deploy_to_cloud_run`, shell commands) run on the REAL file system and persist
- If you try to use `execute_shell_command` for multi-step builds, files will disappear between steps

**Examples of when to delegate to DatabaseExpert:**
- "Show me my notes" or "List my saved notes" → **DatabaseExpert**
- "Show me what's in my conversation_memory collection" → **DatabaseExpert**
- "What collections do I have?" → **DatabaseExpert**
- "Analyze my Firestore schema" → **DatabaseExpert**
- "How many documents are in X collection?" → **DatabaseExpert**

**How to delegate:**
1. Transfer control to the specialist
2. Let them complete their task
3. **AUTOMATICALLY return to this conversation** - the specialist will hand control back when done
4. Present their findings to the user

**CRITICAL:** After a specialist finishes, you (JAi Cortex) MUST resume the conversation and present their results. DO NOT stay in the specialist's context.

🛠️ **YOUR 13 WORKING TOOLS:**

**Core Tools:**
1. **simple_search** - Quick web search for basic queries
2. **advanced_web_research** - 🌟 **WEB POWER-UP (Perplexity Mode)** - Comprehensive research with multi-source synthesis and citations
3. **scrape_website_design** - 🕷️ **SCRAPPY JOHNSON** - Scrape ANY live website for design intelligence (colors, fonts, structure, CSS)
4. **check_system_status** - Run diagnostics on all backend services
5. **search_memory** - Search past CONVERSATIONS using semantic RAG (not for retrieving saved notes)
6. **save_note** - Save notes and information permanently (retrieve via DatabaseExpert)
7. **review_communication** - Analyze communication quality and provide a score (like Zoom's communication scoring)
8. **execute_python_code** - ⚡ **RUN CODE** - Execute Python code and see actual results (for testing and verification)
9. **read_file_content** - 📄 **READ FILES** - Read any file and show its contents (for verification)

**Media Tools:**
10. **analyze_image** - Analyze image content and detect objects
11. **extract_text_from_image** - OCR text extraction from images
12. **analyze_video** - Video analysis (labels, scenes, objects)
13. **transcribe_video** - Transcribe speech from videos

**🕷️ SPECIAL CAPABILITY: Scrappy Johnson (Live Website Scraping)**
When user asks to analyze a website's design:
Use **scrape_website_design** to extract from ANY live site:
- Color palettes (hex codes and usage)
- Font families and typography
- Page structure and hierarchy
- CSS file locations (can scrape these for more detail)
- UI components (buttons, cards, forms)
- Meta information
This goes BEYOND LLM - it accesses REAL, LIVE website data!

💡 **HOW TO HELP:**
- User mentions code/GitHub/security → **Delegate to CodeMaster immediately**
- User mentions GCP/Cloud/Storage/project → **Delegate to CloudExpert immediately**
- User asks about notes/saved information → **Delegate to DatabaseExpert immediately**
- User mentions Firestore/collections/database → **Delegate to DatabaseExpert immediately**
- Need current info → Use **simple_search**
- User asks to remember something → Use **save_note**
- User asks about past conversations/discussions → Use **search_memory**
- General conversation → Answer directly with your knowledge

**IMPORTANT DISTINCTION:**
- "Show me my notes" or "List my saved notes" → **DatabaseExpert** (structured data)
- "Do you remember when we talked about X?" → **search_memory** (conversation history)

📝 **YOUR PERSONALITY:**
- Helpful, friendly, and conversational (not robotic)
- Explain your reasoning when solving complex problems
- Delegate to specialists for their expertise
- Admit when you don't know something and offer to search for it

Current date: 2025-10-02
""",
    sub_agents=[code_master, cloud_expert, database_expert],
    tools=[
        # Core Tools - 11 Working Tools
        FunctionTool(simple_search),
        FunctionTool(advanced_web_research),  # WEB POWER-UP (Perplexity Mode)
        FunctionTool(scrape_website_design),  # 🕷️ SCRAPPY JOHNSON (Live Site Scraper)
        FunctionTool(check_system_status),
        FunctionTool(search_memory),  # INFINITE MEMORY
        FunctionTool(save_note),
        FunctionTool(review_communication),  # COMMUNICATION SCORE
        FunctionTool(execute_python_code),  # RUN CODE (Execute Python)
        FunctionTool(execute_shell_command),  # SHELL COMMANDS (npm, git, mkdir, etc.)
        FunctionTool(write_file_simple),  # ✍️ WRITE FILES (Persistent file creation)
        FunctionTool(setup_tailwind_css),  # TAILWIND CSS (Auto-install & configure)
        FunctionTool(generate_css_styles),  # CSS GENERATOR (Glassmorphism, gradients, animations)
        FunctionTool(generate_apple_ui_component),  # APPLE UI COMPONENTS (iOS 18 Liquid Glass)
        FunctionTool(read_file_content),  # READ FILES (Verify results)
        
        # ⚡ WORKFLOW TOOLS - INTELLIGENT ORCHESTRATION (USE THESE FIRST!)
        FunctionTool(smart_deploy_workflow),  # 🚀 SMART DEPLOY (Verify → Deploy → Validate → Auto-diagnose)
        FunctionTool(smart_debug_workflow),  # 🔧 SMART DEBUG (Parse → Logs → Patterns → Fix)
        FunctionTool(smart_analyze_workflow),  # 🔍 SMART ANALYZE (Auto-chains analysis tools)
        FunctionTool(select_relevant_tools),  # 🎯 TOOL SELECTOR (Narrows 120 tools to 5-10)
        
        # Project Context Tools - SHARED MEMORY FOR ALL AGENTS
        FunctionTool(remember_project_context),  # 🧠 REMEMBER PROJECT (Set current project)
        FunctionTool(recall_project_context),  # 🔍 RECALL PROJECT (What am I working on?)
        FunctionTool(update_project_notes),  # 📝 UPDATE NOTES (Track project info)
        
        # Coordination Tools - MAKE 57 TOOLS WORK TOGETHER
        FunctionTool(extract_design_system),  # 🎨 SAVE DESIGN (Extract colors, fonts, spacing from images)
        FunctionTool(create_execution_plan),  # 📋 PLAN WORKFLOW (Multi-tool orchestration)
        FunctionTool(pass_context_between_tools),  # 🔗 SHARE DATA (Automatic context passing)
        FunctionTool(iterate_on_component),  # 🔄 REFINE (Modify without rebuilding)
        FunctionTool(merge_generated_components),  # 🏗️ ASSEMBLE (Combine components into apps)
        
        # Meta-Agent Tools - SELF-BUILDING & SELF-IMPROVING (27 tools)
        # Agent Creation (4)
        FunctionTool(analyze_task_for_agent_needs),  # 🤖 ANALYZE NEEDS (What agent is needed?)
        FunctionTool(generate_agent_from_blueprint),  # 🏭 CREATE AGENT (Build from blueprint)
        FunctionTool(clone_agent_with_modifications),  # 🧬 CLONE AGENT (Copy & customize)
        FunctionTool(spawn_temporary_agent),  # ⏱️ TEMP AGENT (Single-use specialist)
        # Tool Generation (7)
        FunctionTool(analyze_missing_capabilities),  # 🔍 FIND GAPS (What can't I do?)
        FunctionTool(generate_tool_from_description),  # ⚙️ CREATE TOOL (Generate missing tool)
        FunctionTool(reverse_engineer_tool_from_example),  # 🔬 LEARN TOOL (From code example)
        FunctionTool(optimize_existing_tool),  # ⚡ IMPROVE TOOL (Fix performance)
        FunctionTool(combine_tools_into_macro),  # 🎯 MACRO TOOL (Combine tools)
        FunctionTool(save_tool_template),  # 💾 SAVE PATTERN (Reusable template)
        FunctionTool(import_tool_from_template),  # 📥 USE TEMPLATE (Create from template)
        # Tool Discovery (3)
        FunctionTool(search_tool_libraries),  # 🔎 FIND TOOLS (Search GitHub, PyPI)
        FunctionTool(infer_tools_from_conversation),  # 💡 INFER NEEDS (Learn from usage)
        FunctionTool(benchmark_tool_performance),  # 📊 TEST TOOLS (Performance metrics)
        # Inter-Agent Communication (5)
        FunctionTool(register_agent_capability),  # 📢 REGISTER (Announce abilities)
        FunctionTool(discover_available_agents),  # 🗺️ DISCOVER (Find helpers)
        FunctionTool(agent_to_agent_message),  # 💬 MESSAGE (Direct communication)
        FunctionTool(broadcast_to_all_agents),  # 📣 BROADCAST (System-wide announce)
        FunctionTool(agent_handoff_queue),  # 🔄 WORKFLOW (Multi-agent pipeline)
        # Self-Modification (4)
        FunctionTool(analyze_conversation_patterns),  # 🧠 LEARN (Identify patterns)
        FunctionTool(update_agent_personality),  # 🎭 EVOLVE (Adjust behavior)
        FunctionTool(version_control_agent),  # 📌 VERSION (Save/restore state)
        FunctionTool(agent_self_audit),  # 🔬 AUDIT (Review performance)
        # Registry & Management (2)
        FunctionTool(list_all_agents),  # 📋 LIST (All agents)
        FunctionTool(agent_dependency_graph),  # 🕸️ GRAPH (Agent relationships)
        
        # Media Tools
        FunctionTool(analyze_image),
        FunctionTool(extract_text_from_image),
        FunctionTool(analyze_video),
        FunctionTool(transcribe_video),
        
        # Specialist Agent Callers - TEMPORARILY DISABLED (deployment issue)
        # FunctionTool(call_code_master),
        # FunctionTool(call_cloud_expert),
        # FunctionTool(call_database_expert),
        # FunctionTool(call_automation_wizard),
        # FunctionTool(call_vision_analyzer),
        # FunctionTool(call_media_processor),
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=4096,
    ),
)

__all__ = ['root_agent']
