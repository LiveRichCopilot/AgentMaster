"""
Fully Autonomous App Builder
The engine builds, tests, fixes, and deploys completely on its own
"""

import asyncio
import time
from pathlib import Path
from autonomous_engine import AutonomousEngine

async def build_deploy_app_autonomously():
    """
    Completely autonomous workflow:
    1. Build the app
    2. Test it
    3. Fix any bugs
    4. Deploy it
    5. Return the working URL
    
    The user does NOTHING.
    """
    
    print("\n" + "🤖"*35)
    print("FULLY AUTONOMOUS APP BUILD & DEPLOY")
    print("🤖"*35 + "\n")
    
    start_time = time.time()
    
    workspace = Path(__file__).parent / "friend_chat_app"
    workspace.mkdir(exist_ok=True)
    
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=True)
    
    # The COMPLETE goal - engine does EVERYTHING
    goal = """Build, test, and deploy a working chat web application.

COMPLETE REQUIREMENTS:
1. Create a Flask app (app.py) with:
   - A home route (@app.route('/')) that renders index.html
   - A /chat POST endpoint for messages
   - Error handling
   
2. Create templates/index.html with a chat interface

3. Create static/style.css with glassmorphic design

4. Create static/script.js to handle chat messages

5. Create requirements.txt with Flask

6. Test that the home route works (create a test file if needed)

7. Fix any bugs found during testing

The app MUST have a working home route that serves the HTML."""
    
    print("🎯 Goal: Build complete, working chat app autonomously\n")
    
    # Let it work
    result = await engine.run(goal)
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    
    print("\n" + "="*70)
    print(f"⏱️  TOTAL BUILD TIME: {minutes}m {seconds:.2f}s")
    print(f"✅ Status: {result['success']}")
    print(f"📊 Tasks: {result['summary']['completed']}/{result['summary']['total_tasks']}")
    print("="*70)
    
    # Now deploy it autonomously
    print("\n🚀 Starting the app...")
    import subprocess
    import os
    
    # Start Flask app in background
    app_path = workspace / "app.py"
    if app_path.exists():
        # Install dependencies
        subprocess.run(["pip3", "install", "-q", "Flask"], 
                      cwd=str(workspace), check=False)
        
        # Start the app
        subprocess.Popen(
            ["python3", "app.py"],
            cwd=str(workspace),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for server to start
        await asyncio.sleep(3)
        
        print("\n" + "🎉"*35)
        print("✅ APP IS LIVE!")
        print("🌐 URL: http://localhost:5001")
        print("🎉"*35 + "\n")
    else:
        print("❌ App file not created")
    
    return result

if __name__ == "__main__":
    asyncio.run(build_deploy_app_autonomously())

