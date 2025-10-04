"""Test if Vertex AI mode actually works with custom tools"""

import os
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'studio-2416451423-f2d96'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from typing import Dict, Any

# Simple custom tool
def test_tool(message: str, tool_context: ToolContext) -> Dict[str, Any]:
    """A test tool to verify custom tools work.
    
    Args:
        message: The message to echo back
    """
    return {"status": "success", "echo": f"Tool received: {message}"}

# Create agent with custom tool
test_agent = Agent(
    name="test_vertex_agent",
    model="gemini-2.5-flash",
    description="Test agent to verify Vertex AI custom tools work",
    instruction="You are a test agent. When asked to test, use the test_tool.",
    tools=[test_tool]
)

print("✅ Agent created successfully!")
print(f"📋 Agent has {len(test_agent.tools)} tool(s): {[t.__name__ if hasattr(t, '__name__') else str(t) for t in test_agent.tools]}")
print("\nNow testing agent execution...")

from google.genai import types as genai_types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Create session
session_service = InMemorySessionService()

async def run_test():
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    runner = Runner(
        agent=test_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    print("\n🚀 Sending test message...")
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text="Please use the test tool with message 'hello vertex'")]
        ),
    ):
        if event.is_final_response():
            print(f"✅ Response: {event.content.parts[0].text if event.content.parts else 'No text'}")
        
        if event.get_function_calls():
            for fc in event.get_function_calls():
                print(f"🛠️  Tool called: {fc.name} with args: {fc.args}")

import asyncio
asyncio.run(run_test())


