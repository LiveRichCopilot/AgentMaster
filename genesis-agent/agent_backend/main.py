"""
FastAPI server for Agent Master.
Serves the ADK agent with proper endpoints for the frontend.
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types as genai_types
from jai_cortex import root_agent  # JAi Cortex OS - Complete ADK with all specialists
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="JAi Cortex OS API", version="3.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistent session service using SQLite database (saves conversation history locally)
session_service = DatabaseSessionService("sqlite:///./jai_cortex_sessions.db")

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    image: Optional[str] = None  # Base64 encoded image
    session_id: str = "default"
    user_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Dict[str, Any]] = []
    generated_image: Optional[Dict[str, str]] = None
    timestamp: int


@app.on_event("startup")
async def startup_event():
    """Initialize default session on startup."""
    try:
        await session_service.create_session(
            app_name="agent_master",
            user_id="default",
            session_id="default"
        )
        print("✅ JAi CORTEX OS - COMPLETE ADK is ready!")
        print("📡 Listening for requests on http://localhost:8000")
        print("🤖 24 Specialist Agents: CodeMaster, CloudExpert, DatabaseExpert, WebSearcher, and 20 more")
        print("🛠️  Core Tools: google_search, save_note, search_notes, upload_file, generate_image_prompt")
        print("⚡ Specialist Tools: call_code_master, call_cloud_expert, call_database_expert, and more")
        print("☁️  Cloud Services: Vertex AI Agent Engine, Cloud Storage, Firestore")
        print("📊 Cloud Trace: ENABLED - Monitor agent delegation and tool execution")
        print("   View traces: https://console.cloud.google.com/traces/list?project=studio-2416451423-f2d96")
    except Exception as e:
        print(f"⚠️  Session already exists or startup error: {e}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - runs the TRUE AGENT with real tools.
    """
    try:
        # Always ensure session exists
        session_key = f"{request.user_id}:{request.session_id}"
        try:
            await session_service.create_session(
                app_name="jai_cortex",
                user_id=request.user_id,
                session_id=request.session_id
            )
        except Exception as e:
            # Session might already exist, that's fine
            print(f"Session creation note: {e}")
            pass
        
        # Create runner with the agent (AdkApp with tracing enabled)
        runner = Runner(
            agent=root_agent,  # This is now an AdkApp with enable_tracing=True
            app_name="jai_cortex",
            session_service=session_service
        )
        
        # Prepare the message content
        parts = [genai_types.Part.from_text(text=request.message)]
        
        # Add image if provided
        if request.image:
            parts.append(genai_types.Part(
                inline_data=genai_types.Blob(
                    mime_type="image/jpeg",
                    data=request.image
                )
            ))
        
        user_message = genai_types.Content(role="user", parts=parts)
        
        # Run the agent with Cloud Trace enabled
        # Traces will show:
        # - Each tool call (web_search, save_note, call_code_master, etc.)
        # - Specialist agent delegations to Vertex AI
        # - LLM interactions and response times
        response_text = ""
        tool_calls = []
        generated_image = None
        
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=request.session_id,
            new_message=user_message
        ):
            # Collect text responses
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
                    # Check for generated images (Nano Banana)
                    if part.inline_data:
                        generated_image = {
                            'mimeType': part.inline_data.mime_type,
                            'data': part.inline_data.data
                        }
            
            # Collect tool usage info
            if event.get_function_calls():
                for func_call in event.get_function_calls():
                    tool_calls.append({
                        'name': func_call.name,
                        'args': dict(func_call.args) if func_call.args else {}
                    })
        
        return ChatResponse(
            response=response_text or "I'm processing that for you...",
            tool_calls=tool_calls,
            generated_image=generated_image,
            timestamp=int(asyncio.get_event_loop().time() * 1000)
        )
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "JAi Cortex OS - Complete ADK",
        "framework": "Google Agent Development Kit",
        "version": "3.0.0",
        "specialists": 24,
        "deployed_agents": "Vertex AI Agent Engine"
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "JAi Cortex OS",
        "description": "Complete AI development team with 24 specialist agents powered by Google ADK",
        "version": "3.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health"
        },
        "core_tools": [
            "google_search",
            "save_note",
            "search_notes",
            "upload_file",
            "generate_image_prompt"
        ],
        "specialist_agents": {
            "CodeMaster": "Full-stack development and debugging",
            "CloudExpert": "Google Cloud Platform infrastructure",
            "DatabaseExpert": "Database management and SQL",
            "WebSearcher": "Internet research",
            "FileManager": "Cloud storage and file operations",
            "MediaProcessor": "Video, audio, image processing",
            "VisionAnalyzer": "Image analysis and OCR",
            "AutomationWizard": "Workflow automation",
            "...and 16 more": "Email, Calendar, Security, Notebooks, etc."
        },
        "deployment": {
            "platform": "Vertex AI Agent Engine",
            "project": "studio-2416451423-f2d96",
            "location": "us-central1"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
