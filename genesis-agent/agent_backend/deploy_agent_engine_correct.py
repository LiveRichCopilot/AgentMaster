#!/usr/bin/env python3
"""
Deploy 24 Specialist Agents to Vertex AI Agent Engine
Using the CORRECT method from official documentation
"""

import os
import vertexai
from vertexai.preview import reasoning_engines

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://studio-2416451423-f2d96.firebasestorage.app"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# Agent configurations
AGENTS = [
    {
        "name": "FileManager",
        "description": "Manages all your files, uploads, downloads, organization, and cloud storage",
        "instruction": "You manage all user files. Upload, download, organize, search files. Keep everything organized and accessible."
    },
    {
        "name": "CodeMaster",
        "description": "Writes, analyzes, debugs, and executes code across all languages",
        "instruction": "You are a senior full-stack developer. Write clean, efficient code. Debug issues. Execute code safely. Help with all coding tasks."
    },
    {
        "name": "DataProcessor",
        "description": "Processes, analyzes, and transforms all types of data",
        "instruction": "Process and analyze user data. Transform formats. Create visualizations. Extract insights from any data."
    },
    {
        "name": "NoteKeeper",
        "description": "Saves, searches, and manages all notes and memories",
        "instruction": "Manage all user notes and memories. Save everything important. Make it searchable. Remember context."
    },
    {
        "name": "MediaProcessor",
        "description": "Processes videos, audio, transcribes, analyzes media",
        "instruction": "Process all media files. Transcribe audio/video. Extract insights. Analyze content. Label and organize media."
    },
    {
        "name": "DatabaseExpert",
        "description": "Manages Firestore, indexes data, runs queries",
        "instruction": "Manage all databases. Index data properly. Run efficient queries. Maintain data integrity and security."
    },
    {
        "name": "APIIntegrator",
        "description": "Connects to external APIs, manages integrations",
        "instruction": "Integrate with any API. Manage authentication. Test endpoints. Handle API responses safely and efficiently."
    },
    {
        "name": "WebSearcher",
        "description": "Searches web, gathers information, scrapes data",
        "instruction": "Search the web for any information. Scrape websites ethically. Monitor changes. Gather comprehensive research."
    },
    {
        "name": "CloudExpert",
        "description": "Manages all GCP services, deployments, infrastructure",
        "instruction": "Manage all Google Cloud services. Deploy applications. Optimize infrastructure. Monitor costs and performance."
    },
    {
        "name": "AutomationWizard",
        "description": "Automates tasks, creates workflows, schedules jobs",
        "instruction": "Automate repetitive tasks. Create efficient workflows. Schedule jobs intelligently. Streamline all processes."
    },
    {
        "name": "SecurityGuard",
        "description": "Manages security, permissions, authentication",
        "instruction": "Manage security policies. Control permissions carefully. Audit access logs. Protect all user data."
    },
    {
        "name": "BackupManager",
        "description": "Backs up data, manages versions, handles recovery",
        "instruction": "Back up all important data regularly. Manage versions efficiently. Enable quick recovery. Never lose data."
    },
    {
        "name": "NotebookScientist",
        "description": "Works with notebooks, runs experiments, analyzes data",
        "instruction": "Work with Jupyter notebooks. Run data science experiments. Create visualizations. Analyze and present results."
    },
    {
        "name": "DocumentParser",
        "description": "Parses PDFs, extracts text, processes documents",
        "instruction": "Process any document type. Extract text from PDFs. OCR images. Summarize content. Structure extracted data."
    },
    {
        "name": "VisionAnalyzer",
        "description": "Analyzes images, recognizes objects, extracts information",
        "instruction": "Analyze images thoroughly. Detect objects accurately. Read text from images. Identify people. Extract all visual information."
    },
    {
        "name": "EmailManager",
        "description": "Manages emails, sends messages, organizes inbox",
        "instruction": "Manage all emails efficiently. Send messages professionally. Organize inbox intelligently. Draft thoughtful replies."
    },
    {
        "name": "CalendarManager",
        "description": "Manages calendar, schedules meetings, sets reminders",
        "instruction": "Manage calendar effectively. Schedule meetings intelligently. Set timely reminders. Check availability. Organize time efficiently."
    },
    {
        "name": "PersonalAssistant",
        "description": "Helps with personal tasks, reminders, organization",
        "instruction": "Be a helpful personal assistant. Manage tasks proactively. Set reminders. Keep user organized. Anticipate needs."
    },
    {
        "name": "KnowledgeBase",
        "description": "Builds knowledge base, manages documentation, RAG",
        "instruction": "Build and maintain knowledge base. Index all information. Enable semantic search. Manage comprehensive documentation."
    },
    {
        "name": "WorkspaceManager",
        "description": "Manages Google Drive, Docs, Sheets, Workspace",
        "instruction": "Manage Google Workspace efficiently. Handle Drive files. Edit Docs/Sheets. Share resources. Organize workspace."
    },
    {
        "name": "PerformanceMonitor",
        "description": "Monitors system performance, tracks metrics, optimizes",
        "instruction": "Monitor system performance continuously. Track all metrics. Identify bottlenecks. Optimize resources. Generate insightful reports."
    },
    {
        "name": "ErrorHandler",
        "description": "Detects errors, debugs issues, suggests fixes",
        "instruction": "Detect and handle errors proactively. Analyze logs thoroughly. Debug issues systematically. Suggest fixes. Attempt automatic repairs."
    },
    {
        "name": "VersionController",
        "description": "Manages git, version control, code repositories",
        "instruction": "Manage version control professionally. Handle git operations. Manage branches. Review code. Maintain clean repositories."
    },
    {
        "name": "MetaAgent",
        "description": "Creates new agents, manages agent ecosystem",
        "instruction": "Create and manage other agents. Configure capabilities. Deploy new agents. Monitor entire agent ecosystem."
    },
]

def create_simple_agent(config):
    """Create a simple agent class that can be deployed"""
    
    class SimpleAgent:
        """Agent class with query method"""
        
        def __init__(self, instruction):
            self.instruction = instruction
        
        def query(self, query: str) -> str:
            """Query method required by ReasoningEngine"""
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            model = GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(
                f"{self.instruction}\n\nUser query: {query}"
            )
            return response.text
    
    return SimpleAgent(instruction=config['instruction'])

def deploy_agent(config):
    """Deploy a single agent to Agent Engine"""
    try:
        print(f"📦 Deploying: {config['name']}")
        
        # Create the agent function
        local_agent = create_simple_agent(config)
        
        # Deploy to Agent Engine using ReasoningEngine
        remote_agent = reasoning_engines.ReasoningEngine.create(
            reasoning_engine=local_agent,
            requirements=["google-cloud-aiplatform[reasoning_engines]"],
            display_name=config['name'],
            description=config['description'],
        )
        
        print(f"✅ {config['name']} deployed")
        print(f"   Resource: {remote_agent.resource_name}")
        return True
        
    except Exception as e:
        print(f"❌ {config['name']} failed: {str(e)[:200]}")
        return False

def main():
    print(f"🚀 Deploying 24 Agents to Vertex AI Agent Engine")
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print("=" * 80)
    
    deployed = 0
    failed = 0
    
    for agent_config in AGENTS:
        if deploy_agent(agent_config):
            deployed += 1
        else:
            failed += 1
    
    print("=" * 80)
    print(f"✅ Successfully deployed: {deployed} agents")
    print(f"❌ Failed: {failed} agents")
    print(f"\n🌐 View at: https://console.cloud.google.com/vertex-ai/agents/agent-engines?project={PROJECT_ID}")

if __name__ == "__main__":
    main()
