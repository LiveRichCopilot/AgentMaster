"""
CORTEX OS - MINIMAL VERSION (matching test_vertex.py that WORKED)
"""

# MUST import vertex_config FIRST to configure Vertex AI
import vertex_config

from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import google_search, ToolContext
from google.genai import types as genai_types

# ONE simple custom tool (like test_vertex.py)
def save_note(title: str, content: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Save a note to memory.
    
    Args:
        title: Title of the note
        content: Content to save
    """
    return {
        "status": "success",
        "message": f"Note '{title}' saved with content: {content}"
    }

# Agent with just 2 tools (google_search + save_note)
cortex_os_agent = Agent(
    name="cortex_minimal",
    model="gemini-2.5-flash",
    description="Minimal Cortex OS for testing",
    instruction="""You are Cortex OS - a helpful AI assistant.

You have 2 tools:
- `google_search`: Search the web for current information
- `save_note`: Save notes and information

Use tools when appropriate. Be friendly and helpful!

Current date: 2025-09-30
""",
    tools=[google_search, save_note],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=2048,
    ),
)
