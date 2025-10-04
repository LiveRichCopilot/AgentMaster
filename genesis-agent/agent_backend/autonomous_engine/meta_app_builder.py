"""
Meta App Builder - True Closed-Loop Autonomy
The system that builds, verifies, fixes, and repeats until 100% working
"""

import asyncio
import time
import subprocess
import requests
from pathlib import Path
from autonomous_engine import AutonomousEngine
from .resilient_llm import ResilientLLM

class MetaAppBuilder:
    """
    True autonomous system with closed-loop feedback:
    1. Build
    2. Deploy
    3. Verify (test it works)
    4. If failed: Analyze error + Fix + Repeat
    5. If success: Done
    """
    
    def __init__(self, workspace_dir: str):
        self.workspace = Path(workspace_dir)
        self.engine = AutonomousEngine(workspace_dir=str(self.workspace), use_llm=True)
        self.llm = ResilientLLM()  # Resilient LLM with fallbacks
        self.server_process = None
        self.port = 5001
        self.max_attempts = 10  # Increased for resilience
        
    async def build_and_deploy(self, goal: str) -> bool:
        """
        Step 1 & 2: Build the app and deploy it
        """
        print(f"\n{'='*70}")
        print(f"🔨 BUILDING APPLICATION")
        print(f"{'='*70}\n")
        
        # Build with autonomous engine
        result = await self.engine.run(goal)
        
        if not result['success']:
            print(f"❌ Build failed")
            return False
            
        print(f"✅ Build complete: {result['summary']['completed']} tasks")
        
        # Deploy
        print(f"\n🚀 DEPLOYING APPLICATION...\n")
        return self.deploy()
        
    def deploy(self) -> bool:
        """Deploy the Flask app"""
        # Kill any existing server
        subprocess.run(["pkill", "-f", "python3 app.py"], 
                      stderr=subprocess.DEVNULL, check=False)
        time.sleep(1)
        
        # Install dependencies
        app_path = self.workspace / "app.py"
        if not app_path.exists():
            print(f"❌ app.py not found")
            return False
            
        subprocess.run(
            ["pip3", "install", "-q", "Flask"],
            cwd=str(self.workspace),
            check=False
        )
        
        # Start server
        self.server_process = subprocess.Popen(
            ["python3", "app.py"],
            cwd=str(self.workspace),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        print(f"✅ Server started on port {self.port}")
        return True
        
    def verify_app(self) -> tuple[bool, str]:
        """
        Step 3: Verify the app actually works
        Returns: (success, error_message)
        """
        print(f"\n{'='*70}")
        print(f"🔍 VERIFYING APPLICATION")
        print(f"{'='*70}\n")
        
        url = f"http://localhost:{self.port}"
        
        try:
            # Test 1: Home page loads
            print(f"Test 1: GET {url}")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Home page loads successfully")
                
                # Test 2: Chat endpoint exists
                print(f"\nTest 2: POST {url}/chat")
                chat_response = requests.post(
                    f"{url}/chat",
                    json={"message": "test"},
                    timeout=5
                )
                
                if chat_response.status_code == 200:
                    print(f"✅ Chat endpoint works")
                    print(f"\n{'='*70}")
                    print(f"✅ ALL TESTS PASSED - APP IS WORKING!")
                    print(f"{'='*70}\n")
                    return (True, "")
                else:
                    error = f"Chat endpoint failed: {chat_response.status_code} - {chat_response.text}"
                    print(f"❌ {error}")
                    return (False, error)
            else:
                error = f"Home page failed: {response.status_code}\n{response.text}"
                print(f"❌ {error}")
                return (False, error)
                
        except requests.exceptions.ConnectionError as e:
            error = f"Cannot connect to server: {str(e)}"
            print(f"❌ {error}")
            return (False, error)
        except Exception as e:
            error = f"Verification error: {str(e)}"
            print(f"❌ {error}")
            return (False, error)
            
    async def diagnose_and_fix(self, error_message: str) -> bool:
        """
        Step 4: Analyze the error and fix it autonomously
        """
        print(f"\n{'='*70}")
        print(f"🔧 AUTONOMOUS ERROR ANALYSIS & FIX")
        print(f"{'='*70}\n")
        
        # Read the current app.py
        app_file = self.workspace / "app.py"
        if not app_file.exists():
            print(f"❌ app.py not found")
            return False
            
        current_code = app_file.read_text()
        
        # Use LLM to diagnose and fix
        fix_prompt = f"""You are an expert Flask developer. The application has this error:

ERROR:
{error_message}

CURRENT CODE (app.py):
{current_code}

TASK:
1. Analyze the error
2. Identify the root cause
3. Generate the COMPLETE, FIXED version of app.py

Requirements:
- The app MUST have a @app.route('/') that serves templates/index.html
- The app MUST have a @app.route('/chat', methods=['POST']) endpoint
- Include all necessary imports
- Return ONLY the fixed Python code, no explanations"""

        print(f"🤖 Calling Gemini to diagnose and fix...\n")
        
        try:
            # Use LLM to generate fix
            fixed_code = await self.llm.generate_code(
                task_description=fix_prompt,
                filename="app.py",
                language="python",
                framework="flask"
            )
            
            # Write the fixed code
            app_file.write_text(fixed_code)
            print(f"✅ Fixed code written to app.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Fix generation failed: {e}")
            return False
            
    async def run(self, goal: str) -> dict:
        """
        Main autonomous loop: Build → Deploy → Verify → Fix → Repeat
        """
        start_time = time.time()
        
        print(f"\n{'🤖'*35}")
        print(f"META APP BUILDER - TRUE CLOSED-LOOP AUTONOMY")
        print(f"{'🤖'*35}\n")
        print(f"Goal: {goal}\n")
        
        attempt = 0
        
        while attempt < self.max_attempts:
            attempt += 1
            print(f"\n{'#'*70}")
            print(f"ATTEMPT {attempt}/{self.max_attempts}")
            print(f"{'#'*70}\n")
            
            # Step 1 & 2: Build and Deploy
            if attempt == 1:
                success = await self.build_and_deploy(goal)
                if not success:
                    print(f"❌ Build/Deploy failed")
                    continue
            else:
                # On retry, just redeploy
                success = self.deploy()
                if not success:
                    print(f"❌ Deploy failed")
                    continue
            
            # Step 3: Verify
            success, error = self.verify_app()
            
            if success:
                # SUCCESS! We're done
                elapsed = time.time() - start_time
                minutes = int(elapsed // 60)
                seconds = elapsed % 60
                
                print(f"\n{'🎉'*35}")
                print(f"SUCCESS! APPLICATION IS FULLY WORKING!")
                print(f"{'🎉'*35}\n")
                print(f"⏱️  Total time: {minutes}m {seconds:.2f}s")
                print(f"🔄 Attempts: {attempt}")
                print(f"🌐 URL: http://localhost:{self.port}\n")
                print(f"{'='*70}\n")
                
                return {
                    'success': True,
                    'attempts': attempt,
                    'elapsed_time': elapsed,
                    'url': f'http://localhost:{self.port}'
                }
            
            # Step 4: Fix the error
            print(f"\n⚠️  App failed verification, attempting autonomous fix...\n")
            
            fixed = await self.diagnose_and_fix(error)
            
            if not fixed:
                print(f"❌ Could not generate fix")
                continue
                
            print(f"✅ Fix applied, will retry deployment...\n")
            
        # Max attempts reached
        print(f"\n{'❌'*35}")
        print(f"FAILED: Could not achieve working state after {self.max_attempts} attempts")
        print(f"{'❌'*35}\n")
        
        return {
            'success': False,
            'attempts': attempt,
            'error': 'Max attempts reached'
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()


async def main():
    """Run the meta app builder"""
    
    workspace = Path(__file__).parent / "friend_chat_app"
    workspace.mkdir(exist_ok=True)
    
    builder = MetaAppBuilder(workspace_dir=str(workspace))
    
    goal = """Build a complete Flask web chat application.

REQUIREMENTS:
1. Flask backend (app.py) with:
   - @app.route('/') that renders templates/index.html
   - @app.route('/chat', methods=['POST']) for chat messages
   - Proper imports (Flask, render_template, jsonify, request)
   
2. templates/index.html - HTML chat interface

3. static/style.css - Glassmorphic styling

4. static/script.js - Chat functionality

5. requirements.txt with Flask

The app MUST be fully functional."""
    
    try:
        result = await builder.run(goal)
        return result
    finally:
        builder.cleanup()


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result['success'] else 1)

