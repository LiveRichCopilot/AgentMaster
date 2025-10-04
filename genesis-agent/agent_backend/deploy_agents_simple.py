#!/usr/bin/env python3
"""
Deploy 24 Agents to Vertex AI Agent Engine using REST API
"""

import subprocess
import json

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

AGENTS = [
    {"name": "FileManager", "desc": "Manages all files, uploads, downloads, organization"},
    {"name": "CodeMaster", "desc": "Writes, analyzes, debugs code across all languages"},
    {"name": "DataProcessor", "desc": "Processes and analyzes all types of data"},
    {"name": "NoteKeeper", "desc": "Saves and searches all notes and memories"},
    {"name": "MediaProcessor", "desc": "Processes videos, audio, transcribes media"},
    {"name": "DatabaseExpert", "desc": "Manages Firestore, indexes data, runs queries"},
    {"name": "APIIntegrator", "desc": "Connects to external APIs, manages integrations"},
    {"name": "WebSearcher", "desc": "Searches web, gathers information, scrapes data"},
    {"name": "CloudExpert", "desc": "Manages all GCP services and infrastructure"},
    {"name": "AutomationWizard", "desc": "Automates tasks, creates workflows"},
    {"name": "SecurityGuard", "desc": "Manages security, permissions, authentication"},
    {"name": "BackupManager", "desc": "Backs up data, manages versions, recovery"},
    {"name": "NotebookScientist", "desc": "Works with notebooks, runs experiments"},
    {"name": "DocumentParser", "desc": "Parses PDFs, extracts text from documents"},
    {"name": "VisionAnalyzer", "desc": "Analyzes images, recognizes objects"},
    {"name": "EmailManager", "desc": "Manages emails, sends messages, organizes inbox"},
    {"name": "CalendarManager", "desc": "Manages calendar, schedules meetings, reminders"},
    {"name": "PersonalAssistant", "desc": "Helps with personal tasks and organization"},
    {"name": "KnowledgeBase", "desc": "Builds knowledge base, manages documentation"},
    {"name": "WorkspaceManager", "desc": "Manages Google Drive, Docs, Sheets, Workspace"},
    {"name": "PerformanceMonitor", "desc": "Monitors system performance and metrics"},
    {"name": "ErrorHandler", "desc": "Detects errors, debugs issues, suggests fixes"},
    {"name": "VersionController", "desc": "Manages git, version control, repositories"},
    {"name": "MetaAgent", "desc": "Creates and manages other agents"}
]

def deploy_agent_rest(agent):
    """Deploy using REST API via curl"""
    
    payload = {
        "displayName": agent["name"],
        "description": agent["desc"],
        "defaultLanguageCode": "en"
    }
    
    url = f"https://{LOCATION}-dialogflow.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}/agents"
    
    cmd = [
        "curl", "-X", "POST", url,
        "-H", f"Authorization: Bearer $(gcloud auth print-access-token)",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if result.returncode == 0 and "name" in result.stdout:
            print(f"✅ {agent['name']} deployed")
            return True
        else:
            print(f"❌ {agent['name']} failed: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"❌ {agent['name']} error: {e}")
        return False

def main():
    print(f"🚀 Deploying {len(AGENTS)} Agents to Vertex AI")
    print(f"📍 Project: {PROJECT_ID}, Location: {LOCATION}")
    print("=" * 60)
    
    deployed = 0
    for agent in AGENTS:
        if deploy_agent_rest(agent):
            deployed += 1
    
    print("=" * 60)
    print(f"✅ Deployed: {deployed}/{len(AGENTS)} agents")
    print(f"\n🌐 View at: https://console.cloud.google.com/vertex-ai/agents?project={PROJECT_ID}")

if __name__ == "__main__":
    main()

