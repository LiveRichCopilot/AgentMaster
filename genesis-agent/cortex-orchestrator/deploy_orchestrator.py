#!/usr/bin/env python3
"""
Deploy Cortex Orchestrator to Vertex AI Agent Engine

DOCUMENTATION: Based on codemaster-agent/app/agent_engine_app.py
Uses vertexai.Client and agent_engines.create() API
"""

import datetime
import json
import logging
import os
import sys
from pathlib import Path

import vertexai
from vertexai._genai.types import AgentEngineConfig
from google.cloud import storage

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app import get_root_agent

logging.basicConfig(level=logging.INFO)

PROJECT = "studio-2416451423-f2d96"
LOCATION = "us-central1"
AGENT_NAME = "Cortex Orchestrator"
STAGING_BUCKET = f"gs://cortex_agent_staging"

def ensure_bucket_exists(bucket_name: str):
    """Ensure GCS bucket exists"""
    client = storage.Client(project=PROJECT)
    bucket_name_only = bucket_name.replace("gs://", "")
    
    try:
        client.get_bucket(bucket_name_only)
        logging.info(f"✅ Bucket {bucket_name} exists")
    except Exception:
        logging.info(f"📦 Creating bucket {bucket_name}...")
        bucket = client.create_bucket(bucket_name_only, location=LOCATION)
        logging.info(f"✅ Created bucket {bucket.name}")

def deploy():
    """Deploy the Cortex Orchestrator"""
    logging.info("🚀 Starting deployment...")
    
    # Ensure bucket exists
    ensure_bucket_exists(STAGING_BUCKET.replace("gs://", ""))
    
    # Initialize Vertex AI
    client = vertexai.Client(project=PROJECT, location=LOCATION)
    vertexai.init(project=PROJECT, location=LOCATION)
    
    # Get the root agent
    logging.info("📦 Loading root_agent...")
    root_agent = get_root_agent()
    logging.info(f"✅ Loaded agent: {root_agent.name}")
    
    # Read requirements from file
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        with open(requirements_file) as f:
            requirements = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        logging.info(f"📋 Using requirements: {requirements}")
    else:
        requirements = ["google-cloud-aiplatform[adk,agent_engines]==1.116.0"]
        logging.info(f"⚠️ No requirements.txt found, using default: {requirements}")
    
    # Configuration
    config = AgentEngineConfig(
        display_name=AGENT_NAME,
        description="Cortex OS - Orchestrator coordinating 23 specialist agents",
        extra_packages=["./app"],
        requirements=requirements,
        staging_bucket=STAGING_BUCKET,
        env_vars={"NUM_WORKERS": "1"},
    )
    
    # Check for existing agent
    logging.info("🔍 Checking for existing deployment...")
    existing_agents = list(client.agent_engines.list())
    matching_agents = [
        agent for agent in existing_agents
        if agent.api_resource.display_name == AGENT_NAME
    ]
    
    if matching_agents:
        logging.info(f"♻️  Updating existing agent: {AGENT_NAME}")
        remote_agent = client.agent_engines.update(
            name=matching_agents[0].api_resource.name,
            agent=root_agent,
            config=config,
        )
    else:
        logging.info(f"🆕 Creating new agent: {AGENT_NAME}")
        remote_agent = client.agent_engines.create(
            agent=root_agent,
            config=config,
        )
    
    # Save metadata
    metadata = {
        "remote_agent_engine_id": remote_agent.api_resource.name,
        "deployment_timestamp": datetime.datetime.now().isoformat(),
        "display_name": AGENT_NAME,
    }
    
    with open("deployment_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    logging.info(f"✅ Agent Engine ID: {remote_agent.api_resource.name}")
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print(f"Agent Name: {AGENT_NAME}")
    print(f"Resource ID: {remote_agent.api_resource.name}")
    print(f"Project: {PROJECT}")
    print(f"Location: {LOCATION}")
    print("="*60 + "\n")
    
    return remote_agent

if __name__ == "__main__":
    try:
        deploy()
    except Exception as e:
        logging.error(f"❌ Deployment failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
