#!/usr/bin/env python3
"""Add webhook to existing Dialogflow CX Agent"""

from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.protobuf import duration_pb2

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
AGENT_ID = "a2057937-0cd2-4923-b71e-7d7e87909fd9"
BACKEND_URL = "https://cortex-os-1096519851619.us-central1.run.app"

def main():
    print("\n🔗 ADDING WEBHOOK TO CORTEX OS AGENT\n")
    
    agent_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}"
    
    # Create webhook
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}
    client = dialogflow.WebhooksClient(client_options=client_options)
    
    webhook = dialogflow.Webhook(
        display_name="Cortex Backend",
        generic_web_service=dialogflow.Webhook.GenericWebService(
            uri=f"{BACKEND_URL}/api/chat",
            request_headers={
                "Content-Type": "application/json"
            }
        ),
        timeout=duration_pb2.Duration(seconds=30),
    )
    
    print("Creating webhook...")
    response = client.create_webhook(parent=agent_name, webhook=webhook)
    print(f"✅ Webhook created: {response.display_name}")
    print(f"   Webhook ID: {response.name.split('/')[-1]}")
    
    print(f"\n✅ WEBHOOK ADDED!\n")
    print(f"🎯 Test your agent at:")
    print(f"https://dialogflow.cloud.google.com/cx/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/test\n")

if __name__ == "__main__":
    main()
