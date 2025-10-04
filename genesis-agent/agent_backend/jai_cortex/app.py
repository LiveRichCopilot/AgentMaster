"""
ADK App configuration for JAi Cortex with persistent session storage
"""

from vertexai.agent_engines import AdkApp
from google.adk.sessions import VertexAiSessionService
from .agent import root_agent

# Session service builder function (called by AdkApp to create the service)
def build_session_service():
    """Builder function for VertexAiSessionService - uses environment variables"""
    return VertexAiSessionService()

# Create ADK app with persistent sessions
app = AdkApp(
    agent=root_agent,
    session_service_builder=build_session_service,
    enable_tracing=True  # Also enable Cloud Trace for monitoring
)

__all__ = ['app', 'root_agent']

