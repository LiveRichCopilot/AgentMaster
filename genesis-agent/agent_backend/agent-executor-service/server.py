from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
import httpx

# --- Configuration ---
PORT = int(os.environ.get("PORT", 8080))
VIDEO_PROCESSING_SERVICE_URL = os.environ.get("VIDEO_PROCESSING_SERVICE_URL")

# --- Mock Tool Implementations ---
async def mock_image_generate(args: dict):
    """Simulates generating an image based on a prompt."""
    prompt = args.get("prompt", "a default image")
    print(f"Executing MOCK tool: image_generate with prompt: '{prompt}'")
    return {"status": "success", "result": f"Mock image generated with prompt: '{prompt}'"}

# --- Real Tool Implementations ---
async def real_video_analyze(args: dict):
    """Makes a live API call to the video-processing-service."""
    print(f"Executing REAL tool: video_analyze with args: {args}")
    if not VIDEO_PROCESSING_SERVICE_URL:
        print("Error: VIDEO_PROCESSING_SERVICE_URL is not configured.")
        raise HTTPException(status_code=500, detail="VIDEO_PROCESSING_SERVICE_URL is not configured.")

    analyze_url = f"{VIDEO_PROCESSING_SERVICE_URL}/analyze"
    print(f"Forwarding request to: {analyze_url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(analyze_url, json=args, timeout=30.0)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except httpx.RequestError as exc:
            print(f"Error calling video-processing-service: {exc}")
            raise HTTPException(status_code=503, detail=f"Error calling video-processing-service: {exc}")

# --- Tool Registry ---
TOOL_REGISTRY = {
    "image_generate": mock_image_generate,
    "video_analyze": real_video_analyze,  # <-- This is now a real API call
}

# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    print("Agent Executor Service starting up...")
    yield
    print("Agent Executor Service shutting down.")

# --- Application ---
app = FastAPI(
    title="Agent Executor Service",
    description="Routes tasks to the appropriate tool or agent.",
    version="1.2.0",
    lifespan=lifespan
)

# --- Data Models ---
class ExecutionRequest(BaseModel):
    tool_name: str
    tool_args: dict = {}

# --- API Endpoints ---
@app.get("/", tags=["Status"])
async def read_root():
    """Confirms the server is running."""
    return {"message": "Agent Executor Service is active."}

@app.post("/execute", tags=["Execution"])
async def execute_tool(request: ExecutionRequest):
    """
    Receives a tool execution request and routes it to the correct tool.
    """
    tool_name = request.tool_name
    tool_args = request.tool_args
    
    print(f"Received execution request for tool: '{tool_name}'")

    if tool_name not in TOOL_REGISTRY:
        print(f"Error: Tool '{tool_name}' not found in registry.")
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")

    tool_function = TOOL_REGISTRY[tool_name]
    result = await tool_function(tool_args)

    return {
        "status": "executed",
        "tool_name": tool_name,
        "result": result
    }

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
