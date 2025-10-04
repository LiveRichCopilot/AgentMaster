from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
import uuid
from google.cloud import videointelligence_v1 as videointelligence

# --- Configuration ---
PORT = int(os.environ.get("PORT", 8080))

# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    print("Video Processing Service starting up...")
    # Initialize the async client once and reuse it.
    app.state.video_client = videointelligence.VideoIntelligenceServiceAsyncClient()
    print("Video Intelligence client initialized.")
    yield
    print("Video Processing Service shutting down.")

# --- Application ---
app = FastAPI(
    title="Video Processing Service",
    description="Handles video analysis, transcoding, and other processing tasks.",
    version="1.1.0",
    lifespan=lifespan
)

# --- Data Models ---
class VideoAnalysisRequest(BaseModel):
    gcs_uri: str
    # Use the official Feature enum for type safety
    features: list[videointelligence.Feature] = [videointelligence.Feature.LABEL_DETECTION]

# --- API Endpoints ---
@app.get("/", tags=["Status"])
async def read_root():
    """Confirms the server is running."""
    return {"message": "Video Processing Service is active."}

@app.post("/analyze", tags=["Analysis"])
async def analyze_video(request: VideoAnalysisRequest, fastapi_request: FastAPI.Request):
    """
    Starts a long-running video analysis job using the Google Cloud Video Intelligence API.
    """
    print(f"Received real analysis request for video: {request.gcs_uri}")
    print(f"Features requested: {request.features}")

    # Get the client from the application state
    video_client = fastapi_request.app.state.video_client

    # Construct the request and call the async method
    operation = await video_client.annotate_video(
        request={
            "input_uri": request.gcs_uri,
            "features": request.features,
        }
    )
    
    job_id = operation.operation.name
    print(f"Started video analysis job. Operation name (Job ID): {job_id}")

    return {
        "status": "submitted",
        "job_id": job_id,  # This ID is used to check the job status later
        "gcs_uri": request.gcs_uri,
        "message": "Video analysis job successfully submitted to Google Cloud."
    }

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
