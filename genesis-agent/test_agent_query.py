"""
Test if deployed agents have query() interface
Based on ADK documentation from notebooks/adk_app_testing.ipynb

DOCUMENTATION SOURCE: codemaster-agent/notebooks/adk_app_testing.ipynb line 66
  client = vertexai.Client(location=LOCATION)
"""
import asyncio
import vertexai

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
CODEMASTER_RESOURCE = "projects/1096519851619/locations/us-central1/reasoningEngines/9119881604401987584"

async def test_agent_query():
    print("🔍 Testing CodeMaster agent query interface...")
    print(f"📍 Resource: {CODEMASTER_RESOURCE}")
    print("")
    
    # Initialize Vertex AI client (from documentation line 66)
    client = vertexai.Client(location=LOCATION)
    
    try:
        # Get the deployed agent (from documentation)
        print("⏳ Loading agent...")
        remote_agent = client.agent_engines.get(name=CODEMASTER_RESOURCE)
        print(f"✅ Agent loaded: {remote_agent}")
        print("")
        
        # Check what methods are available
        print("📋 Available methods:")
        methods = [method for method in dir(remote_agent) if not method.startswith('_')]
        for method in methods:
            print(f"   - {method}")
        print("")
        
        # Try to query (from documentation)
        print("🧪 Testing async_stream_query...")
        async for event in remote_agent.async_stream_query(
            message="Hello! What is your name and role?",
            user_id="test_user"
        ):
            print(f"📨 Event: {event}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent_query())
