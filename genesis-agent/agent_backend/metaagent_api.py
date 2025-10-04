"""
JAi Cortex MetaAgent API - Backend for Chat UI
Connects glassmorphic UI to deployed Agent Engine agents
Version: 3.0 - Agent Engine Integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import json
import vertexai
from vertexai import agent_engines
from google.cloud import firestore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://cortex_agent_staging"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
)

# Load deployed CodeMaster agent
CODEMASTER_RESOURCE = "projects/1096519851619/locations/us-central1/reasoningEngines/3180196645853724672"
codemaster_agent = agent_engines.get(CODEMASTER_RESOURCE)

logger.info(f"✅ Loaded CodeMaster agent: {CODEMASTER_RESOURCE}")

app = FastAPI(title="JAi Cortex MetaAgent API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[dict]
    session_id: str
    success: bool

@app.post("/chat/working", response_model=ChatResponse)
async def chat_working(request: ChatRequest):
    """
    JAi Cortex endpoint - NOW USING DEPLOYED CODEMASTER AGENT!
    Connects to Agent Engine for real agent processing with tools
    """
    try:
        logger.info(f"🤖 Routing to CodeMaster: {request.message}")
        
        # Query the deployed CodeMaster agent
        response = codemaster_agent.query(
            message=request.message,
            user_id=request.session_id or "default"
        )
        
        logger.info(f"✅ CodeMaster response received")
        
        return ChatResponse(
            response=str(response),
            tool_calls=[],  # TODO: Extract tool calls from agent response
            session_id=request.session_id or "default",
            success=True
        )
    except Exception as e:
        logger.error(f"CodeMaster error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "JAi Cortex"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Force rebuild Tue Sep 30 18:22:56 PDT 2025
