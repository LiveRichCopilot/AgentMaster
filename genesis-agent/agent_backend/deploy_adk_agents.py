#!/usr/bin/env python3
"""
Deploy 24 Specialist Agents to Vertex AI Agent Engine
Using ADK framework (recommended by Google)
"""

import os
import vertexai
from vertexai.preview import reasoning_engines
from google import genai
from google.genai import types

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://studio-2416451423-f2d96.firebasestorage.app"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# Agent configurations
AGENTS = [
    {
        "name": "FileManager",
        "description": "Manages all your files, uploads, downloads, organization, and cloud storage",
        "instruction": "You manage all user files. Upload, download, organize, search files. Keep everything organized and accessible."
    },
    {
        "name": "CodeMaster",
        "description": "Writes, analyzes, debugs, and executes code across all languages",
        "instruction": "You are a senior full-stack developer. Write clean, efficient code. Debug issues. Execute code safely. Help with all coding tasks."
    },
    {
        "name": "DataProcessor",
        "description": "Processes, analyzes, and transforms all types of data",
        "instruction": "Process and analyze user data. Transform formats. Create visualizations. Extract insights from any data."
    },
    {
        "name": "NoteKeeper",
        "description": "Saves, searches, and manages all notes and memories",
        "instruction": "Manage all user notes and memories. Save everything important. Make it searchable. Remember context."
    },
]

def create_adk_agent(config):
    """Create an ADK agent"""
    
    class ADKAgent:
        """ADK-compatible agent"""
        
        def __init__(self, instruction: str, model_name: str = "gemini-2.0-flash-exp"):
            self.instruction = instruction
            self.model_name = model_name
        
        def query(self, query: str) -> dict:
            """Query method for ADK"""
            try:
                # Initialize client inside query method (lazy initialization)
                client = genai.Client(
                    vertexai=True,
                    project=PROJECT_ID,
                    location=LOCATION
                )
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=f"{self.instruction}\n\nUser query: {query}"
                )
                return {"response": response.text}
            except Exception as e:
                return {"error": str(e)}
    
    return ADKAgent(instruction=config['instruction'])

def deploy_agent(config):
    """Deploy a single agent to Agent Engine"""
    try:
        print(f"📦 Deploying: {config['name']}")
        
        # Create the ADK agent
        local_agent = create_adk_agent(config)
        
        # Deploy to Agent Engine
        remote_agent = reasoning_engines.ReasoningEngine.create(
            reasoning_engine=local_agent,
            requirements=[
                "google-cloud-aiplatform[reasoning_engines]",
                "google-genai"
            ],
            display_name=config['name'],
            description=config['description'],
        )
        
        print(f"✅ {config['name']} deployed")
        print(f"   Resource: {remote_agent.resource_name}")
        return True
        
    except Exception as e:
        print(f"❌ {config['name']} failed: {str(e)[:300]}")
        return False

def main():
    print(f"🚀 Deploying Agents to Vertex AI Agent Engine (ADK)")
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print("=" * 80)
    
    deployed = 0
    failed = 0
    
    for agent_config in AGENTS:
        if deploy_agent(agent_config):
            deployed += 1
        else:
            failed += 1
        print()
    
    print("=" * 80)
    print(f"✅ Successfully deployed: {deployed} agents")
    print(f"❌ Failed: {failed} agents")
    print(f"\n🌐 View at: https://console.cloud.google.com/vertex-ai/reasoning-engines?project={PROJECT_ID}")

if __name__ == "__main__":
    main()
