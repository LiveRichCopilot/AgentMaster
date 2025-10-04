#!/usr/bin/env python3
"""
Deploy 24 Specialist Agents to Vertex AI Agent Engine
Using the correct agent_engines API
"""

import os
import vertexai
from vertexai import agent_engines
from google.adk.agents import Agent
from google.adk.agents.llms import Model

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-bucket"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# Agent configurations
AGENTS_CONFIG = [
    {
        "name": "file_manager",
        "display_name": "File & Data Manager",
        "description": "Manages all your files, uploads, downloads, organization, and cloud storage",
        "instruction": "You manage all user files. Upload, download, organize, search files. Keep everything organized."
    },
    {
        "name": "code_master",
        "display_name": "Senior Developer",
        "description": "Writes, analyzes, debugs, and executes code",
        "instruction": "You are a senior full-stack developer. Write clean code. Debug issues. Execute code safely."
    },
    {
        "name": "data_processor",
        "display_name": "Data Analyst",
        "description": "Processes and analyzes all types of data",
        "instruction": "Process and analyze data. Transform formats. Create visualizations. Extract insights."
    },
    {
        "name": "note_keeper",
        "display_name": "Note Manager",
        "description": "Saves and searches notes and memories",
        "instruction": "Manage all user notes. Save everything. Make it searchable. Remember context."
    },
    {
        "name": "media_processor",
        "display_name": "Media Processor",
        "description": "Processes videos, audio, transcribes media",
        "instruction": "Process media files. Transcribe audio/video. Analyze content. Label and organize."
    },
    {
        "name": "database_expert",
        "display_name": "Database Manager",
        "description": "Manages Firestore, indexes data, runs queries",
        "instruction": "Manage databases. Index data. Run efficient queries. Maintain integrity."
    },
    {
        "name": "api_integrator",
        "display_name": "API Specialist",
        "description": "Connects to external APIs",
        "instruction": "Integrate with APIs. Manage authentication. Test endpoints. Handle responses."
    },
    {
        "name": "web_searcher",
        "display_name": "Web Researcher",
        "description": "Searches web, gathers information",
        "instruction": "Search the web. Scrape websites. Monitor changes. Gather research."
    },
]

def create_and_deploy_agent(config):
    """Create and deploy a single agent to Agent Engine"""
    try:
        print(f"📦 Creating agent: {config['display_name']}")
        
        # Create ADK agent
        agent = Agent(
            name=config['name'],
            model=Model(model_name="gemini-2.0-flash-exp"),
            description=config['description'],
            instruction=config['instruction']
        )
        
        print(f"   Deploying to Agent Engine...")
        
        # Deploy to Agent Engine
        remote_agent = agent_engines.create(
            agent=agent,
            config={
                "display_name": config['display_name'],
                "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            }
        )
        
        print(f"✅ {config['display_name']} deployed: {remote_agent.resource_name}")
        return True
        
    except Exception as e:
        print(f"❌ {config['display_name']} failed: {str(e)[:200]}")
        return False

def list_deployed_agents():
    """List all deployed agents"""
    try:
        print("\n📋 Currently deployed agents:")
        for agent in agent_engines.list():
            print(f"  - {agent.display_name}: {agent.resource_name}")
    except Exception as e:
        print(f"⚠️  Could not list agents: {e}")

def main():
    print(f"🚀 Deploying Agents to Vertex AI Agent Engine")
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print("=" * 80)
    
    deployed = 0
    failed = 0
    
    for agent_config in AGENTS_CONFIG:
        if create_and_deploy_agent(agent_config):
            deployed += 1
        else:
            failed += 1
    
    print("=" * 80)
    print(f"✅ Successfully deployed: {deployed} agents")
    print(f"❌ Failed: {failed} agents")
    
    # List all deployed agents
    list_deployed_agents()
    
    print(f"\n🌐 View at: https://console.cloud.google.com/vertex-ai/agents/agent-engines?project={PROJECT_ID}")

if __name__ == "__main__":
    main()

