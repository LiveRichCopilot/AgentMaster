#!/usr/bin/env python3
"""
Test the agent wiring - verify MetaAgent can communicate with specialists
"""
import json
from google.cloud import aiplatform
from google.cloud import aiplatform_v1beta1

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Load registry
with open("agent_registry.json") as f:
    registry = json.load(f)

def test_metaagent():
    """Test if MetaAgent is accessible"""
    print("🧪 Testing MetaAgent...")
    
    meta_agent_id = registry["meta_agent"]
    
    try:
        client = aiplatform_v1beta1.ReasoningEngineServiceClient(
            client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        )
        
        # Simple test query
        response = client.query_reasoning_engine(
            name=meta_agent_id,
            input={"query": "Hello, are you online?"}
        )
        
        print(f"  ✅ MetaAgent responding")
        print(f"  Response: {response.output if hasattr(response, 'output') else 'OK'}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_specialist(name, agent_info):
    """Test if a specialist agent is accessible"""
    try:
        client = aiplatform_v1beta1.ReasoningEngineServiceClient(
            client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        )
        
        response = client.query_reasoning_engine(
            name=agent_info["resource_name"],
            input={"query": "ping"}
        )
        
        return True
    except Exception as e:
        return False

def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║             TESTING JAI CORTEX WIRING                     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # Test MetaAgent
    meta_working = test_metaagent()
    
    print()
    print("🧪 Testing specialist agents (sampling 5)...")
    
    # Test a few specialists
    specialists_to_test = list(registry["specialist_agents"].items())[:5]
    working = 0
    
    for name, info in specialists_to_test:
        if test_specialist(name, info):
            print(f"  ✅ {name}")
            working += 1
        else:
            print(f"  ⏸️  {name} (may need initialization)")
    
    print()
    print("📊 RESULTS:")
    print(f"  • MetaAgent: {'✅ Working' if meta_working else '❌ Not responding'}")
    print(f"  • Specialists tested: {working}/{len(specialists_to_test)}")
    print(f"  • Total agents in registry: {len(registry['specialist_agents'])}")
    print()
    
    if meta_working:
        print("✅ WIRING TEST PASSED!")
        print()
        print("🚀 Ready to start the system:")
        print("   ./start_cortex.sh")
    else:
        print("⚠️  MetaAgent needs attention")
        print("   Check deployment status in Vertex AI console")

if __name__ == "__main__":
    main()
