"""
Meta App Builder v2.8 - Phase 2.8
Complete verification with browser testing + META-LEARNER
TRUE 100% autonomy with memory and learning
"""

import asyncio
import time
import subprocess
from pathlib import Path
from typing import List
from autonomous_engine import AutonomousEngine
from .resilient_llm import ResilientLLM
from verification_system import VerificationSystem
from meta_learner import MetaLearner


class MetaAppBuilder:
    """
    True autonomous system with complete verification:
    1. Build
    2. Deploy
    3. Verify (build + backend + frontend in browser)
    4. Fix
    5. Repeat until 100% working
    """
    
    def __init__(self, workspace_dir: str):
        self.workspace = Path(workspace_dir)
        self.engine = AutonomousEngine(workspace_dir=str(self.workspace), use_llm=True)
        self.llm = ResilientLLM()
        self.verification_system = VerificationSystem(workspace_dir=str(self.workspace))
        self.meta_learner = MetaLearner()  # 🧠 THE BRAIN
        self.server_process = None
        self.port = 5001
        self.max_attempts = 10
        self.pending_solution = None  # Store fix until verified
        
    async def build_and_deploy(self, goal: str) -> bool:
        """Build the app and deploy it"""
        print(f"\n{'='*70}")
        print(f"🔨 BUILDING APPLICATION")
        print(f"{'='*70}\n")
        
        result = await self.engine.run(goal)
        
        if not result['success']:
            print(f"❌ Build failed")
            return False
            
        print(f"✅ Build complete: {result['summary']['completed']}/{result['summary']['total_tasks']} tasks")
        print(f"\n🚀 DEPLOYING APPLICATION...\n")
        return self.deploy()
        
    def deploy(self) -> bool:
        """Deploy the Flask app"""
        # Kill existing server
        subprocess.run(["pkill", "-f", "python3 app.py"], 
                      stderr=subprocess.DEVNULL, check=False)
        time.sleep(1)
        
        app_path = self.workspace / "app.py"
        if not app_path.exists():
            print(f"❌ app.py not found")
            return False
            
        # Install dependencies
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
        
        time.sleep(3)
        print(f"✅ Server started on port {self.port}")
        return True
        
    async def diagnose_and_fix(self, errors: List[str]) -> bool:
        """
        Use LLM to analyze errors and generate fixes
        FILE-AWARE: Determines which file to fix based on error analysis
        MEMORY-AWARE: Checks if we've seen this error before
        """
        print(f"\n{'='*70}")
        print(f"🔧 AUTONOMOUS ERROR ANALYSIS & FIX (FILE-AWARE + MEMORY)")
        print(f"{'='*70}\n")
        
        error_message = "\n".join(errors)
        
        # Step 0: CHECK MEMORY FIRST! 🧠
        has_solution, solution_data = self.meta_learner.analyze_error(
            errors, 
            files_state={}  # TODO: Pass actual file state
        )
        
        if has_solution and solution_data and not solution_data.get("trigger_self_improvement"):
            # WE'VE SEEN THIS BEFORE!
            print(f"\n{'🎯'*35}")
            print(f"APPLYING KNOWN SOLUTION (No Gemini call needed!)")
            print(f"{'🎯'*35}\n")
            
            # Apply the saved solution
            saved_solution = solution_data['solution']
            
            if 'fixed_content' in saved_solution:
                # We have the exact fix
                file_path = self.workspace / saved_solution['file']
                file_path.write_text(saved_solution['fixed_content'])
                print(f"✅ Applied saved solution to {saved_solution['file']}")
                print(f"⚡ Fixed instantly! (No AI call needed)\n")
                return True
        
        # Step 1: Analyze errors to determine which file to fix (NEW ERROR)
        print(f"🔍 Analyzing NEW error to identify the problem file...\n")
        
        # Determine file type based on error keywords
        file_to_fix = None
        file_path = None
        language = None
        
        if any(keyword in error_message.lower() for keyword in ['selector', '#', 'not visible', 'chat-container', 'message-form', 'html element']):
            file_to_fix = "templates/index.html"
            file_path = self.workspace / "templates" / "index.html"
            language = "html"
            print(f"📄 Problem detected in: HTML (missing/incorrect UI elements)")
            
        elif any(keyword in error_message.lower() for keyword in ['css', 'style', 'stylesheet', 'styling']):
            file_to_fix = "static/style.css"
            file_path = self.workspace / "static" / "style.css"
            language = "css"
            print(f"🎨 Problem detected in: CSS (styling issues)")
            
        elif any(keyword in error_message.lower() for keyword in ['javascript', 'script.js', 'js error', 'console error']):
            file_to_fix = "static/script.js"
            file_path = self.workspace / "static" / "script.js"
            language = "javascript"
            print(f"⚡ Problem detected in: JavaScript (frontend logic)")
            
        elif 'requirements.txt' in error_message.lower():
            file_to_fix = "requirements.txt"
            file_path = self.workspace / "requirements.txt"
            language = "text"
            print(f"📦 Problem detected in: Dependencies (requirements.txt)")
            
        else:
            # Default to backend if unclear
            file_to_fix = "app.py"
            file_path = self.workspace / "app.py"
            language = "python"
            print(f"🐍 Problem detected in: Python backend")
        
        # Step 2: Read the problematic file
        if not file_path.exists():
            print(f"❌ {file_to_fix} not found")
            return False
            
        current_code = file_path.read_text()
        print(f"📖 Current {file_to_fix}: {len(current_code)} characters\n")
        
        # Step 3: Build file-specific fix prompt
        if language == "html":
            fix_prompt = f"""You are an expert frontend developer. The chat application has these HTML errors:

ERRORS:
{error_message}

CURRENT HTML ({file_to_fix}):
{current_code}

CRITICAL REQUIREMENT:
The HTML MUST include these EXACT element IDs (these are NON-NEGOTIABLE):
- id="chat-container" on a div element
- id="message-form" on a form element  
- id="message-input" on an input element
- type="submit" on a button element

EXAMPLE STRUCTURE (you MUST include this):
<!DOCTYPE html>
<html>
<head>
    <title>Chat App</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="chat-container">
        <!-- Chat messages will appear here -->
    </div>
    
    <form id="message-form">
        <input type="text" id="message-input" placeholder="Type a message...">
        <button type="submit">Send</button>
    </form>
    
    <script src="/static/script.js"></script>
</body>
</html>

Return ONLY the complete, corrected HTML code with these EXACT IDs."""

        elif language == "css":
            fix_prompt = f"""You are an expert CSS developer. The application has these styling errors:

ERRORS:
{error_message}

CURRENT CSS ({file_to_fix}):
{current_code}

TASK:
Generate complete, corrected CSS with glassmorphic design.

Return ONLY the fixed CSS code."""

        elif language == "javascript":
            fix_prompt = f"""You are an expert JavaScript developer. The application has these errors:

ERRORS:
{error_message}

CURRENT JS ({file_to_fix}):
{current_code}

TASK:
1. Fix all JavaScript errors
2. Ensure form submission handling works
3. Ensure messages are sent to /chat endpoint
4. Ensure UI updates properly

Return ONLY the fixed JavaScript code."""

        elif language == "text":  # requirements.txt
            fix_prompt = f"""You are an expert Python developer. The requirements.txt file has these errors:

ERRORS:
{error_message}

CURRENT REQUIREMENTS.TXT:
{current_code}

TASK:
Generate a complete requirements.txt file for a Flask web application.

Required dependencies:
- Flask (latest stable version)
- Any other common Flask dependencies

Format: One dependency per line with version pins (e.g., Flask==3.0.0)

Return ONLY the corrected requirements.txt content."""

        else:  # Python
            fix_prompt = f"""You are an expert Flask developer. The application has these errors:

ERRORS:
{error_message}

CURRENT PYTHON ({file_to_fix}):
{current_code}

TASK:
1. Analyze ALL errors
2. Generate COMPLETE, FIXED Flask app

Critical requirements:
- Must have @app.route('/') that renders templates/index.html
- Must have @app.route('/chat', methods=['POST']) endpoint
- Must import Flask, render_template, jsonify, request

Return ONLY the fixed Python code."""

        print(f"🤖 Calling Gemini to fix {file_to_fix}...\n")
        
        try:
            fixed_code = await self.llm.generate_code(
                task_description=fix_prompt,
                filename=file_to_fix,
                language=language,
                framework="flask" if language == "python" else None
            )
            
            file_path.write_text(fixed_code)
            print(f"✅ Fixed code written to {file_to_fix}")
            print(f"📊 New file size: {len(fixed_code)} characters\n")
            
            # DON'T save yet! Wait until we verify it actually works
            # Store the fix temporarily so we can save it AFTER verification
            self.pending_solution = {
                "error_signature": self.meta_learner.create_signature_from_error(error_message),
                "solution": {
                    "file": file_to_fix,
                    "fixed_content": fixed_code,
                    "fix_type": "gemini_generated",
                    "language": language
                }
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Fix generation failed: {e}")
            return False
            
    async def run(self, goal: str, required_files: List[str]) -> dict:
        """
        Main autonomous loop with complete verification
        """
        start_time = time.time()
        
        print(f"\n{'🤖'*35}")
        print(f"META APP BUILDER - PHASE 2.6 (100% AUTONOMY)")
        print(f"{'🤖'*35}\n")
        print(f"Goal: {goal}\n")
        print(f"Required files: {required_files}\n")
        
        attempt = 0
        
        while attempt < self.max_attempts:
            attempt += 1
            print(f"\n{'#'*70}")
            print(f"ATTEMPT {attempt}/{self.max_attempts}")
            print(f"{'#'*70}\n")
            
            # Build and Deploy
            if attempt == 1:
                if not await self.build_and_deploy(goal):
                    continue
            else:
                if not self.deploy():
                    continue
            
            # COMPLETE VERIFICATION (build + backend + frontend)
            success, errors = await self.verification_system.run_all_verifications(required_files)
            
            if success:
                # SUCCESS! NOW save to memory (only save what WORKS!)
                if self.pending_solution:
                    print(f"\n{'💾'*35}")
                    print(f"SAVING VERIFIED SOLUTION TO MEMORY")
                    print(f"{'💾'*35}\n")
                    
                    self.meta_learner.save_successful_solution(
                        self.pending_solution['error_signature'],
                        self.pending_solution['solution']
                    )
                    self.pending_solution = None  # Clear it
                
                elapsed = time.time() - start_time
                minutes = int(elapsed // 60)
                seconds = elapsed % 60
                
                print(f"\n{'🎉'*35}")
                print(f"SUCCESS! APPLICATION IS 100% WORKING!")
                print(f"{'🎉'*35}\n")
                print(f"⏱️  Total time: {minutes}m {seconds:.2f}s")
                print(f"🔄 Attempts: {attempt}")
                print(f"🌐 URL: http://localhost:{self.port}")
                print(f"\n{'='*70}")
                print(f"✅ ALL VERIFICATION CHECKS PASSED:")
                print(f"   ✅ Build integrity")
                print(f"   ✅ Backend functionality")
                print(f"   ✅ Frontend functionality (browser)")
                print(f"{'='*70}\n")
                
                return {
                    'success': True,
                    'attempts': attempt,
                    'elapsed_time': elapsed,
                    'url': f'http://localhost:{self.port}'
                }
            
            # Failed verification - fix and retry
            print(f"\n⚠️  Verification FAILED with {len(errors)} issues")
            print(f"🔧 Attempting autonomous fix...\n")
            
            fixed = await self.diagnose_and_fix(errors)
            
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

CRITICAL REQUIREMENTS - ALL FILES MUST BE CREATED:
1. app.py - Flask backend with:
   - @app.route('/') that renders templates/index.html
   - @app.route('/chat', methods=['POST']) for messages
   - Proper imports (Flask, render_template, jsonify, request)
   
2. templates/index.html - Complete HTML with:
   - Chat container (#chat-container)
   - Message form (#message-form)
   - Message input (#message-input)
   - Send button
   - Links to CSS and JS
   
3. static/style.css - Complete styling with glassmorphic design

4. static/script.js - Complete JavaScript with:
   - Form submission handling
   - Message sending to /chat endpoint
   - UI updates
   
5. requirements.txt with Flask

ALL FILES ARE MANDATORY. Missing ANY file = FAILURE."""
    
    required_files = [
        "app.py",
        "templates/index.html",
        "static/style.css",
        "static/script.js",
        "requirements.txt"
    ]
    
    try:
        result = await builder.run(goal, required_files)
        return result
    finally:
        builder.cleanup()


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result['success'] else 1)

