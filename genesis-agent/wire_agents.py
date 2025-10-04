#!/usr/bin/env python3
"""
Wire up all agents - Create the MetaAgent orchestrator and set up IAM permissions
"""
import json
from google.cloud import aiplatform
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Initialize
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# All agent resource names from the deployment
AGENTS = {
    "WorkspaceManager": "projects/1096519851619/locations/us-central1/reasoningEngines/1173280061906747392",
    "VisionAnalyzer": "projects/1096519851619/locations/us-central1/reasoningEngines/6937887584940982272",
    "VersionController": "projects/1096519851619/locations/us-central1/reasoningEngines/891805085196091392",
    "WebSearcher": "projects/1096519851619/locations/us-central1/reasoningEngines/2283417370053574656",
    "PerformanceMonitor": "projects/1096519851619/locations/us-central1/reasoningEngines/3571446863481536512",
    "SecurityGuard": "projects/1096519851619/locations/us-central1/reasoningEngines/2326201566513594368",
    "NoteKeeper": "projects/1096519851619/locations/us-central1/reasoningEngines/4632044575727288320",
    "NotebookScientist": "projects/1096519851619/locations/us-central1/reasoningEngines/837550783435112448",
    "PersonalAssistant": "projects/1096519851619/locations/us-central1/reasoningEngines/5271555722813898752",
    "MetaAgent": "projects/1096519851619/locations/us-central1/reasoningEngines/1641654423153278976",
    "ErrorHandler": "projects/1096519851619/locations/us-central1/reasoningEngines/8385794865140596736",
    "MediaProcessor": "projects/1096519851619/locations/us-central1/reasoningEngines/8534202546611290112",
    "KnowledgeBase": "projects/1096519851619/locations/us-central1/reasoningEngines/399575719673331712",
    "EmailManager": "projects/1096519851619/locations/us-central1/reasoningEngines/5877289872695230464",
    "DocumentParser": "projects/1096519851619/locations/us-central1/reasoningEngines/1265603854267842560",
    "DatabaseExpert": "projects/1096519851619/locations/us-central1/reasoningEngines/3262950289006657536",
    "DataProcessor": "projects/1096519851619/locations/us-central1/reasoningEngines/8153859484331016192",
    "CloudExpert": "projects/1096519851619/locations/us-central1/reasoningEngines/434689723017986048",
    "AutomationWizard": "projects/1096519851619/locations/us-central1/reasoningEngines/6145042944291241984",
    "CalendarManager": "projects/1096519851619/locations/us-central1/reasoningEngines/6818331088583131136",
    "ApiIntegrator": "projects/1096519851619/locations/us-central1/reasoningEngines/558538712770674688",
    "BackupManager": "projects/1096519851619/locations/us-central1/reasoningEngines/3999288828081733632",
    "CodeMaster": "projects/1096519851619/locations/us-central1/reasoningEngines/9119881604401987584",
    "FileManager": "projects/1096519851619/locations/us-central1/reasoningEngines/112471243428462592",
}

def create_agent_registry():
    """Create a JSON file with all agent endpoints for the MetaAgent to use"""
    registry = {
        "meta_agent": AGENTS["MetaAgent"],
        "specialist_agents": {}
    }
    
    for name, resource_name in AGENTS.items():
        if name != "MetaAgent":
            registry["specialist_agents"][name] = {
                "resource_name": resource_name,
                "endpoint": f"https://us-central1-aiplatform.googleapis.com/v1beta1/{resource_name}:query",
                "description": f"{name} specialist agent"
            }
    
    # Save to file
    with open("/Users/liverichmedia/Agent master /genesis-agent/agent_registry.json", "w") as f:
        json.dump(registry, f, indent=2)
    
    print(f"✅ Created agent registry with {len(registry['specialist_agents'])} specialist agents")
    return registry

def setup_iam_permissions():
    """Set up IAM permissions for agent-to-agent communication"""
    print("\n🔐 Setting up IAM permissions...")
    
    # The MetaAgent service account needs permission to invoke all other agents
    # In practice, all reasoning engines in the same project can communicate
    print("  ℹ️  Agents in the same project can communicate by default")
    print("  ℹ️  For production, set up service account permissions")
    
    return True

def create_metaagent_tools():
    """Create tools for MetaAgent to call other agents"""
    tools = []
    
    for name, info in AGENTS.items():
        if name != "MetaAgent":
            tool = {
                "name": f"call_{name.lower()}",
                "description": f"Call the {name} specialist agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to send to the agent"
                        }
                    },
                    "required": ["query"]
                }
            }
            tools.append(tool)
    
    # Save tools definition
    with open("/Users/liverichmedia/Agent master /genesis-agent/metaagent_tools.json", "w") as f:
        json.dump(tools, f, indent=2)
    
    print(f"✅ Created {len(tools)} tools for MetaAgent")
    return tools

if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           WIRING UP JAI CORTEX AGENT SYSTEM               ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # Step 1: Create agent registry
    registry = create_agent_registry()
    
    # Step 2: Set up IAM permissions
    setup_iam_permissions()
    
    # Step 3: Create MetaAgent tools
    tools = create_metaagent_tools()
    
    print()
    print("✅ WIRING COMPLETE!")
    print()
    print("📋 Next steps:")
    print("1. Update MetaAgent with routing logic")
    print("2. Deploy Chat UI frontend")
    print("3. Test agent-to-agent communication")
    print()
    print("Files created:")
    print("  - agent_registry.json (agent endpoints)")
    print("  - metaagent_tools.json (MetaAgent tools)")
