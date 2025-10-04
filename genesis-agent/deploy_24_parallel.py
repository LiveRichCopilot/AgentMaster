#!/usr/bin/env python3
"""
Deploy all 24 specialist agents to Vertex AI Agent Engine in PARALLEL
Using the proven Agent Starter Pack + Python multiprocessing
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ID = "studio-2416451423-f2d96"
REGION = "us-central1"
BASE_DIR = Path("/Users/liverichmedia/Agent master /genesis-agent")

# All 24 agents
AGENTS = [
    ("FileManager", "Manages all your files, uploads, downloads, organization, and cloud storage"),
    ("CodeMaster", "Writes, analyzes, debugs, and executes code across all languages"),
    ("DataProcessor", "Processes, analyzes, and transforms all types of data"),
    ("NoteKeeper", "Saves, searches, and manages all notes and memories"),
    ("MediaProcessor", "Processes videos, audio, transcribes, analyzes media"),
    ("DatabaseExpert", "Manages Firestore, indexes data, runs queries"),
    ("APIIntegrator", "Connects to external APIs, manages integrations"),
    ("WebSearcher", "Searches web, gathers information, scrapes data"),
    ("CloudExpert", "Manages all GCP services, deployments, infrastructure"),
    ("AutomationWizard", "Automates tasks, creates workflows, schedules jobs"),
    ("SecurityGuard", "Manages security, permissions, authentication"),
    ("BackupManager", "Backs up data, manages versions, handles recovery"),
    ("NotebookScientist", "Works with notebooks, runs experiments, analyzes data"),
    ("DocumentParser", "Parses PDFs, extracts text, processes documents"),
    ("VisionAnalyzer", "Analyzes images, recognizes objects, extracts information"),
    ("EmailManager", "Manages emails, sends messages, organizes inbox"),
    ("CalendarManager", "Manages calendar, schedules meetings, sets reminders"),
    ("PersonalAssistant", "Helps with personal tasks, reminders, organization"),
    ("KnowledgeBase", "Builds knowledge base, manages documentation, RAG"),
    ("WorkspaceManager", "Manages Google Drive, Docs, Sheets, Workspace"),
    ("PerformanceMonitor", "Monitors system performance, tracks metrics, optimizes"),
    ("ErrorHandler", "Detects errors, debugs issues, suggests fixes"),
    ("VersionController", "Manages git, version control, code repositories"),
    ("MetaAgent", "Creates new agents, manages agent ecosystem"),
]

def deploy_agent(agent_info):
    """Deploy a single agent"""
    agent_name, agent_desc = agent_info
    agent_dir = BASE_DIR / f"{agent_name.lower()}-agent"
    
    try:
        # Skip FileManager - already deployed
        if agent_name == "FileManager":
            return (agent_name, "SKIPPED", "Already deployed")
        
        print(f"📦 Creating: {agent_name}")
        
        # Create agent project
        result = subprocess.run(
            [
                "agent-starter-pack", "create", f"{agent_name.lower()}-agent",
                "--agent", "adk_base",
                "--deployment-target", "agent_engine",
                "--region", REGION,
                "--auto-approve"
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if not agent_dir.exists():
            return (agent_name, "FAILED", "Failed to create project")
        
        # Install dependencies
        subprocess.run(
            ["uv", "sync", "--dev"],
            cwd=agent_dir,
            capture_output=True,
            timeout=120
        )
        
        # Export requirements
        with open(agent_dir / ".requirements.txt", "w") as f:
            subprocess.run(
                ["uv", "export", "--no-hashes", "--no-header", "--no-dev", "--no-emit-project"],
                cwd=agent_dir,
                stdout=f,
                stderr=subprocess.PIPE,
                timeout=30
            )
        
        # Deploy to Agent Engine
        print(f"   🚀 Deploying {agent_name} to Agent Engine...")
        result = subprocess.run(
            ["uv", "run", "app/agent_engine_app.py", "--agent-name", agent_name],
            cwd=agent_dir,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per agent
        )
        
        if "Deployment successful" in result.stdout or "Deployment successful" in result.stderr:
            return (agent_name, "SUCCESS", "Deployed successfully")
        else:
            error = result.stderr[:200] if result.stderr else "Unknown error"
            return (agent_name, "FAILED", error)
            
    except subprocess.TimeoutExpired:
        return (agent_name, "TIMEOUT", "Deployment took too long")
    except Exception as e:
        return (agent_name, "ERROR", str(e)[:200])

def main():
    print("🚀 DEPLOYING 24 AGENTS TO VERTEX AI AGENT ENGINE (PARALLEL)")
    print("=" * 80)
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Region: {REGION}")
    print(f"⏱️  Deploying {len(AGENTS)} agents in parallel (5-10 minutes total)")
    print("=" * 80)
    print()
    
    # Deploy in parallel with 6 workers
    deployed = 0
    failed = 0
    skipped = 0
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(deploy_agent, agent): agent for agent in AGENTS}
        
        for future in as_completed(futures):
            agent_name, status, message = future.result()
            
            if status == "SUCCESS":
                print(f"✅ {agent_name}: {message}")
                deployed += 1
            elif status == "SKIPPED":
                print(f"⏭️  {agent_name}: {message}")
                skipped += 1
            else:
                print(f"❌ {agent_name}: {message}")
                failed += 1
    
    print()
    print("=" * 80)
    print(f"✅ Successfully deployed: {deployed} agents")
    print(f"⏭️  Skipped: {skipped} agents")
    print(f"❌ Failed: {failed} agents")
    print()
    print(f"🌐 View all agents:")
    print(f"https://console.cloud.google.com/vertex-ai/reasoning-engines?project={PROJECT_ID}")

if __name__ == "__main__":
    main()
