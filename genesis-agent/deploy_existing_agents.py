#!/usr/bin/env python3
"""Deploy all existing agent projects to Agent Engine"""

import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path("/Users/liverichmedia/Agent master /genesis-agent")

def deploy_agent(agent_dir):
    """Deploy a single existing agent"""
    agent_name = agent_dir.name.replace("-agent", "").title().replace(" ", "")
    
    try:
        print(f"🚀 Deploying: {agent_name}")
        
        # Export requirements if not exists
        req_file = agent_dir / ".requirements.txt"
        if not req_file.exists():
            with open(req_file, "w") as f:
                subprocess.run(
                    ["uv", "export", "--no-hashes", "--no-header", "--no-dev", "--no-emit-project"],
                    cwd=agent_dir,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    timeout=30
                )
        
        # Deploy
        result = subprocess.run(
            ["uv", "run", "app/agent_engine_app.py", "--agent-name", agent_name],
            cwd=agent_dir,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if "Deployment successful" in result.stdout:
            print(f"✅ {agent_name}")
            return (agent_name, "SUCCESS")
        else:
            print(f"❌ {agent_name}: {result.stderr[:100]}")
            return (agent_name, "FAILED")
            
    except Exception as e:
        print(f"❌ {agent_name}: {str(e)[:100]}")
        return (agent_name, "ERROR")

# Get all agent directories
agent_dirs = sorted([d for d in BASE_DIR.glob("*-agent") if d.is_dir()])

print(f"🚀 DEPLOYING {len(agent_dirs)} AGENTS IN PARALLEL")
print("=" * 80)

deployed = 0
failed = 0

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(deploy_agent, d): d for d in agent_dirs}
    
    for future in as_completed(futures):
        agent_name, status = future.result()
        if status == "SUCCESS":
            deployed += 1
        else:
            failed += 1

print("=" * 80)
print(f"✅ Deployed: {deployed}")
print(f"❌ Failed: {failed}")
print(f"\n🌐 https://console.cloud.google.com/vertex-ai/reasoning-engines?project=studio-2416451423-f2d96")

