from fastapi import FastAPI, Request
from pydantic import BaseModel
from google.cloud import firestore
import os
import datetime
from contextlib import asynccontextmanager

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT", "unknown-project")
PORT = int(os.environ.get("PORT", 8080))
BUCKET_NAME = "studio-2416451423-f2d96-v2-assets"
DB_COLLECTION_PREFIX = "v2_"

# --- Lifespan Management for Robust Startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Initializes the ASYNCHRONOUS Firestore client to ensure non-blocking startup.
    """
    # Use the AsyncClient for a non-blocking connection.
    app.state.db = firestore.AsyncClient()
    print("Successfully initialized ASYNCHRONOUS Firestore client.")
    yield
    print("Application shutting down.")


# --- Application ---
app = FastAPI(
    title="Live Agent Server V2",
    description="Second-generation agent service.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Data Models ---
class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None

# --- API Endpoints (all async) ---
@app.get("/", tags=["Status"])
async def read_root():
    """Confirms the server is running."""
    return {"message": "Live Agent Server V2 is active."}

@app.get("/status", tags=["Status"])
async def get_status(request: Request):
    """Provides the operational status and configuration of the service."""
    db_status = "initialized" if hasattr(request.app.state, 'db') and request.app.state.db else "not_initialized"
    return {
        "status": "ok",
        "service_name": "live-agent-server-v2",
        "project_id": PROJECT_ID,
        "storage_bucket": BUCKET_NAME,
        "database_collection_prefix": DB_COLLECTION_PREFIX,
        "database_status": db_status
    }

@app.post("/projects", tags=["Projects"], status_code=201)
async def create_project(project_request: CreateProjectRequest, request: Request):
    """
    Creates a new project record in the database using non-blocking I/O.
    """
    db = request.app.state.db
    projects_collection = db.collection(f"{DB_COLLECTION_PREFIX}projects")
    
    new_project_data = {
        "name": project_request.name,
        "description": project_request.description,
        "created_at": datetime.datetime.utcnow(),
        "status": "new",
        "asset_ids": []
    }
    
    # Use 'await' for the non-blocking database operation.
    update_time, project_ref = await projects_collection.add(new_project_data)
    
    return {
        "message": "Project created successfully.",
        "project_id": project_ref.id,
        "created_at": update_time
    }

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
