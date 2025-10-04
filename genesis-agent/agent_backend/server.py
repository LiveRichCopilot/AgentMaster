"""
FastAPI Server for Cortex OS - Pure Vertex AI
"""

import os
import asyncio
import base64
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from cortex_full import chat, model, PROJECT_ID, LOCATION, TOOL_FUNCTIONS

# Import multi-agent system
try:
    from multi_agent_system import get_agent_manager, get_router
    from platform_webhooks import router as webhook_router
    from agent_templates import AGENT_TEMPLATES
    from media_tools import process_zoom_video_full_impl
    HAS_MULTI_AGENT = True
except Exception as e:
    print(f"⚠️  Multi-agent system not available: {e}")
    HAS_MULTI_AGENT = False

# Initialize FastAPI
app = FastAPI(title="Cortex OS API", version="3.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (simple for now)
sessions: Dict[str, List] = {}

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    image: Optional[str] = None  # Base64 encoded
    session_id: str = "default"
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Dict[str, Any]] = []
    generated_image: Optional[Dict[str, str]] = None
    timestamp: int
    selected_agent: Optional[str] = "Cortex"

@app.on_event("startup")
async def startup_event():
    print("=" * 70)
    print("✅ CORTEX OS - MULTI-AGENT SYSTEM ONLINE!")
    print("=" * 70)
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print(f"🛠️  Total Tools: {len(TOOL_FUNCTIONS)}")
    print(f"☁️  Framework: Pure Vertex AI (No Firebase)")
    print(f"📡 Server: http://localhost:8000")
    print("=" * 70)
    
    if HAS_MULTI_AGENT:
        print("\n🤖 SPECIALIST AGENTS:")
        for name, template in AGENT_TEMPLATES.items():
            print(f"  • {template['name']}: {template['role']}")
        print("\n🌐 PLATFORMS: Web, Telegram, WhatsApp")
        print("📹 MEDIA: Full Zoom video processing")
        print("📊 METRICS: Agent strength monitoring")
    else:
        print("\n⚠️  Multi-agent system: Limited (run: pip install httpx twilio)")
    
    print("\n🎉 READY FOR MULTI-PLATFORM, MULTI-AGENT ACTION!\n")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint with intelligent agent routing"""
    try:
        # Get or create session history
        session_key = f"{request.user_id}:{request.session_id}"
        history = sessions.get(session_key, [])
        
        # INTELLIGENT ROUTING: Route to best specialist agent
        if HAS_MULTI_AGENT:
            router = get_router()
            routing = router.handle_message(
                message=request.message,
                platform='web',
                user_id=request.user_id,
                session_id=request.session_id
            )
            selected_agent = routing.get('agent_id', 'Cortex')
            print(f"🎯 Routing to: {selected_agent}")
        else:
            selected_agent = "Cortex"
        
        # Call Vertex AI agent (main Cortex with all tools)
        result = chat(
            message=request.message,
            image_base64=request.image,
            chat_history=history
        )
        
        # Add agent info to response
        result["selected_agent"] = selected_agent
        
        # Update session history
        sessions[session_key] = result["history"]
        
        return ChatResponse(
            response=result["response"],
            tool_calls=result["tool_calls"],
            generated_image=None,
            timestamp=int(datetime.now().timestamp() * 1000),
            selected_agent=result.get("selected_agent", "Cortex")
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": "Cortex OS",
        "framework": "Vertex AI",
        "version": "3.0.0",
        "project": PROJECT_ID
    }

@app.get("/")
async def root():
    return {
        "name": "Cortex OS - Multi-Agent System",
        "description": "Pure Vertex AI with 8 Specialist Agents + 41 Tools",
        "version": "4.0.0",
        "framework": "Vertex AI (No Firebase)",
        "project": PROJECT_ID,
        "endpoints": {
            "chat": "/api/chat",
            "voice": "ws://localhost:8000/ws/voice",
            "agents": "/api/agents",
            "agent_strength": "/api/agents/{agent_id}/strength",
            "create_agent": "/api/agents/create",
            "upload_video": "/api/upload/video",
            "health": "/api/health",
            "webhooks": "/webhook/{platform}"
        },
        "total_tools": len(TOOL_FUNCTIONS),
        "specialist_agents": list(AGENT_TEMPLATES.keys()) if HAS_MULTI_AGENT else [],
        "platforms": ["web", "telegram", "whatsapp"]
    }

# ============================================================================
# MULTI-AGENT ENDPOINTS
# ============================================================================

@app.get("/api/agents")
async def list_agents():
    """List all specialist agents with their strength"""
    if not HAS_MULTI_AGENT:
        return {"status": "error", "message": "Multi-agent system not available"}
    
    manager = get_agent_manager()
    agents = manager.list_agents()
    
    return {
        "status": "success",
        "total": len(agents),
        "agents": agents
    }

@app.get("/api/agents/{agent_id}/strength")
async def agent_strength(agent_id: str):
    """Get detailed strength metrics for an agent"""
    if not HAS_MULTI_AGENT:
        return {"status": "error", "message": "Multi-agent system not available"}
    
    manager = get_agent_manager()
    strength = manager.get_agent_strength(agent_id)
    
    return strength

class CreateAgentRequest(BaseModel):
    template: str
    custom_name: Optional[str] = None

@app.post("/api/agents/create")
async def create_custom_agent(request: CreateAgentRequest):
    """Create a new specialist agent from template"""
    if not HAS_MULTI_AGENT:
        return {"status": "error", "message": "Multi-agent system not available"}
    
    manager = get_agent_manager()
    result = manager.create_agent(request.template, request.custom_name)
    
    return result

class VideoUploadRequest(BaseModel):
    video_base64: str
    filename: str

@app.post("/api/upload/video")
async def upload_video(request: VideoUploadRequest):
    """Upload and process Zoom video - Full pipeline"""
    if not HAS_MULTI_AGENT:
        return {"status": "error", "message": "Media processing not available"}
    
    result = process_zoom_video_full_impl(request.video_base64, request.filename)
    return result

@app.get("/api/platform/stats")
async def platform_stats():
    """Get statistics across all platforms"""
    if not HAS_MULTI_AGENT:
        return {"status": "error", "message": "Multi-agent system not available"}
    
    router = get_router()
    stats = router.get_platform_stats()
    
    return {
        "status": "success",
        **stats
    }

# Include webhook routes
if HAS_MULTI_AGENT:
    app.include_router(webhook_router)

# ============================================================================
# VOICE WEBSOCKET FOR REAL-TIME CONVERSATION
# ============================================================================

@app.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    """
    Real-time voice conversation WebSocket
    Handles bidirectional audio streaming
    """
    await websocket.accept()
    print("🎤 Voice WebSocket connected")
    
    try:
        from voice_interface import transcribe_audio_stream_impl, text_to_speech_impl
        
        while True:
            # Receive audio data from client
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                # Transcribe incoming audio
                audio_base64 = data.get("audio")
                transcription = transcribe_audio_stream_impl(audio_base64)
                
                if transcription['status'] == 'success':
                    text = transcription['transcript']
                    print(f"🎤 User said: {text}")
                    
                    # Get agent response
                    result = chat(
                        message=text,
                        image_base64=None,
                        chat_history=[]
                    )
                    
                    response_text = result["response"]
                    print(f"🤖 Agent responds: {response_text}")
                    
                    # Convert response to speech
                    tts_result = text_to_speech_impl(response_text)
                    
                    if tts_result['status'] == 'success':
                        # Send audio response back
                        await websocket.send_json({
                            "type": "audio_response",
                            "audio": tts_result['audio_base64'],
                            "text": response_text,
                            "format": "mp3"
                        })
                    else:
                        # Send text only
                        await websocket.send_json({
                            "type": "text_response",
                            "text": response_text
                        })
            
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        print("🎤 Voice WebSocket disconnected")
    except Exception as e:
        print(f"❌ Voice WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
