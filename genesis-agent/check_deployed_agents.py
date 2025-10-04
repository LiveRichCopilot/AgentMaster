#!/usr/bin/env python3
"""Quick check of deployed agents"""
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="studio-2416451423-f2d96", location="us-central1")

agents = list(reasoning_engines.ReasoningEngine.list())

print(f"\n🤖 DEPLOYED TO VERTEX AI AGENT ENGINE: {len(agents)} agents")
print("=" * 80)

for agent in agents:
    agent_id = agent.resource_name.split('/')[-1]
    print(f"✅ {agent.display_name} (ID: {agent_id})")

print("=" * 80)
print(f"\n🌐 View: https://console.cloud.google.com/vertex-ai/reasoning-engines?project=studio-2416451423-f2d96\n")

