"""
MetaAgent - Central orchestrator that routes requests to specialist agents
"""
import json
import os
from typing import Any, Dict
from google.cloud import aiplatform
from google.adk.agents import Agent

# Load agent registry
REGISTRY_PATH = "/Users/liverichmedia/Agent master /genesis-agent/agent_registry.json"
with open(REGISTRY_PATH) as f:
    AGENT_REGISTRY = json.load(f)

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Routing keywords for each agent
ROUTING_MAP = {
    "CodeMaster": ["code", "programming", "debug", "function", "class", "python", "javascript", "developer", "software"],
    "CloudExpert": ["cloud", "gcp", "google cloud", "vertex", "bigquery", "compute engine", "kubernetes", "deploy"],
    "DatabaseExpert": ["database", "sql", "query", "table", "schema", "firestore", "mongodb"],
    "ApiIntegrator": ["api", "integration", "endpoint", "rest", "webhook", "connect"],
    "AutomationWizard": ["automation", "workflow", "automate", "script", "batch"],
    "DataProcessor": ["data processing", "etl", "transform", "pipeline"],
    "DocumentParser": ["document", "pdf", "parse", "extract", "text"],
    "EmailManager": ["email", "gmail", "send email", "inbox"],
    "CalendarManager": ["calendar", "schedule", "meeting", "appointment", "event"],
    "FileManager": ["file", "folder", "upload", "download", "storage"],
    "MediaProcessor": ["video", "audio", "image", "media", "process video"],
    "VisionAnalyzer": ["vision", "image analysis", "ocr", "photo", "lens"],
    "WebSearcher": ["search", "google", "find information", "research", "web"],
    "NotebookScientist": ["notebook", "jupyter", "data science", "analysis"],
    "SecurityGuard": ["security", "vulnerability", "threat", "protect"],
    "KnowledgeBase": ["knowledge", "information", "learn", "remember"],
    "PerformanceMonitor": ["performance", "monitor", "metrics", "speed"],
    "ErrorHandler": ["error", "exception", "bug", "fix", "troubleshoot"],
    "WorkspaceManager": ["workspace", "docs", "sheets", "slides", "google workspace"],
    "PersonalAssistant": ["task", "todo", "reminder", "help me"],
    "NoteKeeper": ["note", "notes", "write down", "remember"],
    "VersionController": ["git", "version", "commit", "branch", "repository"],
    "BackupManager": ["backup", "restore", "recovery", "archive"],
}

def route_query(query: str) -> str:
    """Determine which specialist agent should handle the query"""
    query_lower = query.lower()
    
    # Score each agent based on keyword matches
    scores = {}
    for agent_name, keywords in ROUTING_MAP.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > 0:
            scores[agent_name] = score
    
    # Return the agent with highest score, or default to CodeMaster
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    
    return "CodeMaster"  # Default agent

def call_specialist_agent(agent_name: str, query: str) -> Dict[str, Any]:
    """Call a specialist agent and return the response"""
    
    if agent_name not in AGENT_REGISTRY["specialist_agents"]:
        return {"error": f"Agent {agent_name} not found"}
    
    agent_info = AGENT_REGISTRY["specialist_agents"][agent_name]
    resource_name = agent_info["resource_name"]
    
    try:
        # Use Vertex AI to query the agent
        from google.cloud import aiplatform_v1beta1
        
        client = aiplatform_v1beta1.ReasoningEngineServiceClient(
            client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        )
        
        # Query the agent
        response = client.query_reasoning_engine(
            name=resource_name,
            input={"query": query}
        )
        
        return {
            "agent": agent_name,
            "response": response.output,
            "success": True
        }
        
    except Exception as e:
        return {
            "agent": agent_name,
            "error": str(e),
            "success": False
        }

def meta_agent_query(query: str, context: list = None) -> Dict[str, Any]:
    """
    Main entry point for MetaAgent
    Routes query to appropriate specialist and returns response
    """
    
    # Determine which agent to use
    target_agent = route_query(query)
    
    # Call the specialist agent
    result = call_specialist_agent(target_agent, query)
    
    # Add routing information
    result["routed_to"] = target_agent
    result["query"] = query
    
    return result

# Create the MetaAgent
meta_agent = Agent(
    name="MetaAgent",
    description="Central orchestrator that routes queries to specialist agents",
    instruction="""
    You are the MetaAgent, the central orchestrator of the JAi Cortex system.
    
    Your job is to:
    1. Understand the user's query
    2. Determine which specialist agent is best suited to handle it
    3. Route the query to that agent
    4. Return the response to the user
    
    You have access to 23 specialist agents covering:
    - Code development (CodeMaster)
    - Cloud infrastructure (CloudExpert)
    - Databases (DatabaseExpert)
    - And many more...
    
    Always route to the most appropriate specialist and provide helpful responses.
    """,
    functions=[meta_agent_query]
)

# For ADK deployment
root_agent = meta_agent
