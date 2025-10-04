#!/usr/bin/env python3
"""
Deploy all agents asynchronously - trigger deployments without waiting.
Then check status separately.
"""
import subprocess
import time
import sys
from pathlib import Path

AGENTS = [
    ("apiintegrator-agent", "ApiIntegrator"),
    ("automationwizard-agent", "AutomationWizard"),
    ("calendarmanager-agent", "CalendarManager"),
    ("cloudexpert-agent", "CloudExpert"),
    ("databaseexpert-agent", "DatabaseExpert"),
    ("dataprocessor-agent", "DataProcessor"),
    ("documentparser-agent", "DocumentParser"),
    ("emailmanager-agent", "EmailManager"),
    ("errorhandler-agent", "ErrorHandler"),
    ("knowledgebase-agent", "KnowledgeBase"),
    ("mediaprocessor-agent", "MediaProcessor"),
    ("metaagent-agent", "MetaAgent"),
    ("notebookscientist-agent", "NotebookScientist"),
    ("notekeeper-agent", "NoteKeeper"),
    ("performancemonitor-agent", "PerformanceMonitor"),
    ("personalassistant-agent", "PersonalAssistant"),
    ("securityguard-agent", "SecurityGuard"),
    ("versioncontroller-agent", "VersionController"),
    ("visionanalyzer-agent", "VisionAnalyzer"),
    ("websearcher-agent", "WebSearcher"),
    ("workspacemanager-agent", "WorkspaceManager"),
]

PROJECT = "studio-2416451423-f2d96"
LOCATION = "us-central1"
BASE_DIR = Path("/Users/liverichmedia/Agent master /genesis-agent")

def deploy_one(dir_name, display_name):
    """Deploy a single agent and return immediately (don't wait)."""
    agent_dir = BASE_DIR / dir_name
    
    if not agent_dir.exists():
        print(f"❌ {display_name}: Directory not found")
        return False
    
    if not (agent_dir / "app" / "agent_engine_app.py").exists():
        print(f"❌ {display_name}: No deployment script")
        return False
    
    print(f"🚀 Triggering deployment: {display_name}...")
    
    # Create a modified deploy script that doesn't wait
    deploy_script = f"""
import sys
sys.path.insert(0, '{agent_dir}')

from app.agent_engine_app import deploy_agent_engine_app

try:
    # This will submit the deployment but may timeout while waiting
    # We'll catch the timeout and move on
    deploy_agent_engine_app(
        project="{PROJECT}",
        location="{LOCATION}",
        agent_name="{display_name}",
    )
    print("✅ {display_name} submitted successfully")
except Exception as e:
    if "timeout" in str(e).lower() or "connection" in str(e).lower():
        print(f"⚠️  {display_name} submitted but timed out waiting for completion (this is OK)")
    else:
        print(f"❌ {display_name} failed: {{e}}")
        raise
"""
    
    # Run deployment
    result = subprocess.run(
        ["python3", "-c", deploy_script],
        cwd=agent_dir,
        capture_output=True,
        text=True,
        timeout=180  # 3 minute timeout per agent submission
    )
    
    if result.returncode == 0 or "submitted" in result.stdout:
        print(f"  ✅ {display_name} deployment initiated")
        return True
    else:
        print(f"  ❌ {display_name} failed:")
        print(f"     {result.stderr[:200]}")
        return False

if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║   🚀 ASYNC AGENT DEPLOYMENT TO VERTEX AI 🚀               ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("")
    print("Strategy: Submit all deployments without waiting for completion.")
    print("Then check status separately with check_deployed_agents.py")
    print("")
    
    success_count = 0
    fail_count = 0
    
    for dir_name, display_name in AGENTS:
        try:
            if deploy_one(dir_name, display_name):
                success_count += 1
            else:
                fail_count += 1
        except subprocess.TimeoutExpired:
            print(f"⚠️  {display_name} submission timed out (deployment may still be running)")
            success_count += 1  # Count as success since it was submitted
        except Exception as e:
            print(f"❌ {display_name} error: {e}")
            fail_count += 1
        
        # Small delay between submissions to avoid overwhelming the API
        time.sleep(10)
    
    print("")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                    SUBMISSION SUMMARY                     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"")
    print(f"✅ Submitted: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"")
    print(f"ℹ️  Deployments are processing in the background.")
    print(f"   Run check_deployed_agents.py to see which ones are ready.")
