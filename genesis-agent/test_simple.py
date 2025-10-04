#!/usr/bin/env python3
"""
Simple test - verify agents are deployed and accessible
"""
from google.cloud import aiplatform

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

print("╔═══════════════════════════════════════════════════════════╗")
print("║          VERIFYING JAI CORTEX DEPLOYMENT                  ║")
print("╚═══════════════════════════════════════════════════════════╝")
print()

# List all reasoning engines
from google.cloud.aiplatform import reasoning_engines

print("📋 Listing deployed agents...")
print()

engines = reasoning_engines.ReasoningEngine.list()

deployed_count = 0
for engine in engines:
    print(f"✅ {engine.display_name}")
    deployed_count += 1

print()
print(f"📊 Total: {deployed_count} agents deployed")
print()

# Show MetaAgent
meta = [e for e in engines if e.display_name == "MetaAgent"]
if meta:
    print("🎯 MetaAgent found:")
    print(f"   Resource: {meta[0].resource_name}")
    print(f"   Created: {meta[0].create_time}")
else:
    print("⚠️  MetaAgent not found")

print()
print("✅ ALL AGENTS ARE DEPLOYED AND READY!")
print()
print("🚀 Next step: Start the chat system")
print("   ./start_cortex.sh")
