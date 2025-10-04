#!/usr/bin/env python3
"""Deploy Cortex OS to Vertex AI Agent Engine via Dialogflow CX"""

from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core import operation
from google.protobuf import duration_pb2
import os

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
BACKEND_URL = "https://cortex-os-1096519851619.us-central1.run.app"

def create_agent():
    """Create Dialogflow CX Agent"""
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}
    client = dialogflow.AgentsClient(client_options=client_options)
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"
    
    agent = dialogflow.Agent(
        display_name="Cortex OS - 24 AI Specialists",
        default_language_code="en",
        time_zone="America/Los_Angeles",
        description="Multi-agent system with 24 specialists and 44 tools",
        enable_stackdriver_logging=True,
        enable_spell_correction=True,
    )
    
    print(f"Creating agent in {parent}...")
    response = client.create_agent(parent=parent, agent=agent)
    print(f"✅ Agent created: {response.name}")
    return response

def create_webhook(agent_name):
    """Create webhook to backend"""
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}
    client = dialogflow.WebhooksClient(client_options=client_options)
    
    webhook = dialogflow.Webhook(
        display_name="Cortex Backend",
        generic_web_service=dialogflow.Webhook.GenericWebService(
            uri=f"{BACKEND_URL}/api/chat",
            request_headers={
                "Content-Type": "application/json"
            },
            allowed_ca_certs=[],
        ),
        timeout=duration_pb2.Duration(seconds=30),
    )
    
    print("Creating webhook...")
    response = client.create_webhook(parent=agent_name, webhook=webhook)
    print(f"✅ Webhook created: {response.display_name}")
    return response

def create_flow(agent_name, webhook_name):
    """Create conversation flow"""
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}
    client = dialogflow.FlowsClient(client_options=client_options)
    
    # Get default start flow
    flows = client.list_flows(parent=agent_name)
    start_flow = None
    for flow in flows:
        if "Start" in flow.display_name:
            start_flow = flow
            break
    
    if start_flow:
        print(f"✅ Using default start flow: {start_flow.display_name}")
        return start_flow
    
    return None

def create_intent(agent_name, webhook_name):
    """Create catch-all intent"""
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}
    client = dialogflow.IntentsClient(client_options=client_options)
    
    # Get the start flow
    flows_client = dialogflow.FlowsClient(client_options=client_options)
    flows = flows_client.list_flows(parent=agent_name)
    start_flow = next((f for f in flows if "Start" in f.display_name), None)
    
    if not start_flow:
        print("❌ No start flow found")
        return None
    
    intent = dialogflow.Intent(
        display_name="User Query - All",
        training_phrases=[
            dialogflow.Intent.TrainingPhrase(parts=[
                dialogflow.Intent.TrainingPhrase.Part(text="help me")
            ]),
            dialogflow.Intent.TrainingPhrase(parts=[
                dialogflow.Intent.TrainingPhrase.Part(text="what is")
            ]),
            dialogflow.Intent.TrainingPhrase(parts=[
                dialogflow.Intent.TrainingPhrase.Part(text="show me")
            ]),
        ],
        parameters=[],
    )
    
    print("Creating intent...")
    response = client.create_intent(parent=start_flow.name, intent=intent)
    print(f"✅ Intent created: {response.display_name}")
    return response

def main():
    print("\n🚀 DEPLOYING CORTEX OS TO VERTEX AI AGENT ENGINE\n")
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Backend: {BACKEND_URL}\n")
    
    try:
        # Step 1: Create agent
        agent = create_agent()
        
        # Step 2: Create webhook
        webhook = create_webhook(agent.name)
        
        # Step 3: Create flow (use default)
        flow = create_flow(agent.name, webhook.name)
        
        # Step 4: Create intent
        intent = create_intent(agent.name, webhook.name)
        
        print("\n✅ DEPLOYMENT COMPLETE!\n")
        print(f"Agent Name: {agent.display_name}")
        print(f"Agent ID: {agent.name.split('/')[-1]}")
        print(f"\n🎯 Test your agent at:")
        print(f"https://dialogflow.cloud.google.com/cx/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{agent.name.split('/')[-1]}/test\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("This might mean an agent already exists or API permissions issue.")
        print("\nTry manually via console:")
        print(f"https://console.cloud.google.com/gen-app-builder/engines?project={PROJECT_ID}")

if __name__ == "__main__":
    main()
