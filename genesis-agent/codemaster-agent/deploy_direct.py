#!/usr/bin/env python3
"""
Direct deployment to Agent Engine using vertexai SDK
Bypasses ADK CLI bug with agent_engine_app.py
"""
import os
import vertexai
from vertexai import agent_engines
from app.agent import root_agent

# Initialize Vertex AI
PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://cortex_agent_staging"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
)

print(f"🚀 Deploying CodeMaster to Agent Engine...")
print(f"   Project: {PROJECT_ID}")
print(f"   Location: {LOCATION}")
print(f"   Staging: {STAGING_BUCKET}")

# Wrap agent for deployment
app_for_engine = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True
)

# Deploy
try:
    remote_app = agent_engines.create(
        app_for_engine,
        requirements=[
            "google-cloud-aiplatform[adk,agent-engines]>=1.116.0",
            "google-adk>=0.5.0",
            "requests>=2.31.0",
            "cloudpickle==3.1.1",
            "pydantic==2.11.9"
        ],
        display_name="CodeMaster",
        description="Senior full-stack developer and coding expert",
        extra_packages=["./app"]
    )
    
    print(f"\n✅ SUCCESS! CodeMaster deployed:")
    print(f"   Resource: {remote_app.resource_name}")
    
    # Save deployment info
    with open("deployment_metadata.json", "w") as f:
        import json
        json.dump({
            "resource_name": remote_app.resource_name,
            "display_name": "CodeMaster",
            "project": PROJECT_ID,
            "location": LOCATION
        }, f, indent=2)
    print(f"   Metadata saved to deployment_metadata.json")
    
except Exception as e:
    print(f"\n❌ DEPLOYMENT FAILED:")
    print(f"   Error: {str(e)}")
    import traceback
    traceback.print_exc()

