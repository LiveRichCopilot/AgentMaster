"""
Meta App Builder v3.0 - Phase 2.9
TRUE COGNITIVE AUTONOMY

This version implements JAi's architecture:
- Multiple problem-solving strategies
- Automatic strategy switching when stuck
- Web-assisted learning when local strategies fail
- Complete memory and self-awareness

"The only way to fail is to quit, or keep trying the same thing over and over in a loop."
"""

import asyncio
import time
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from autonomous_engine import AutonomousEngine
from .resilient_llm import ResilientLLM
from verification_system import VerificationSystem
from meta_learner import MetaLearner
from web_learner import WebLearner
from cognitive_supervisor import CognitiveSupervisor
from research_agent import ResearchAgent
from .knowledge_base import KnowledgeBase


class MetaAppBuilderV3:
    """
    The Executor: Carries out builds, verifications, and fixes.
    Now strategy-aware: can execute different approaches based on supervisor's direction.
    """
    
    def __init__(self, workspace_dir: str):
        self.workspace = Path(workspace_dir)
        self.port = 5001
        self.engine = AutonomousEngine(workspace_dir=str(self.workspace), use_llm=True)
        self.llm = ResilientLLM()
        self.verification_system = VerificationSystem(
            workspace_dir=str(self.workspace),
            port=self.port  # Pass port during initialization
        )
        self.meta_learner = MetaLearner()  # 🧠 Memory from experience
        self.web_learner = WebLearner()     # 🌐 Reactive web search
        self.research_agent = ResearchAgent()  # 🔬 Proactive research
        self.knowledge_base = KnowledgeBase()  # 📚 Persistent knowledge
        self.server_process = None
        self.pending_solution = None
        self.last_errors = []  # Store errors from last verification
        self.required_files = [
            "app.py",
            "templates/index.html",
            "static/style.css",
            "static/script.js",
            "requirements.txt"
        ]
        
        # HTML template (the proven solution)
        self.html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Friend Chat</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <form id="message-form">
            <input type="text" id="message-input" placeholder="Type a message..." autocomplete="off">
            <button type="submit">Send</button>
        </form>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>'''
        
    async def run_with_strategy(self, strategy: str) -> Tuple[bool, Optional[str]]:
        """
        Execute one complete cycle with a specific strategy.
        Called by CognitiveSupervisor.
        
        Args:
            strategy: One of ['direct_file_fix', 'contextual_file_fix', 'use_template', 'web_search_for_solution']
        
        Returns:
            (success, error_message)
        """
        # First run: build and deploy
        if not hasattr(self, '_built'):
            success = await self._initial_build()
            if not success:
                return False, "Initial build failed"
            self._built = True
        
        # Run verification
        success, errors = await self.verification_system.run_all_verifications(
            required_files=self.required_files
        )
        
        if success:
            print("\n✅ ALL VERIFICATIONS PASSED!")
            # Save pending solution to memory if we just fixed something
            if self.pending_solution:
                error_sig = self.pending_solution['error_signature']
                solution_data = {
                    'fixed_code': self.pending_solution['fixed_code'],
                    'file_path': self.pending_solution['file_path'],
                    'strategy': strategy
                }
                self.meta_learner.save_successful_solution(error_sig, solution_data)
                print(f"🧠 LEARNED: Saved working solution to memory")
                self.pending_solution = None
            return True, None
        
        # Failed verification - store errors
        self.last_errors = errors
        error_message = "\n".join(self.last_errors)
        
        # Apply the requested strategy
        if strategy == "direct_file_fix":
            success = await self._strategy_direct_file_fix()
        elif strategy == "contextual_file_fix":
            success = await self._strategy_contextual_file_fix()
        elif strategy == "use_template":
            success = await self._strategy_use_template()
        elif strategy == "web_search_for_solution":
            success = await self._strategy_web_search()
        else:
            print(f"⚠️ Unknown strategy: {strategy}")
            success = False
        
        if not success:
            return False, error_message
        
        # Redeploy after fix
        self.deploy()
        
        return False, error_message  # Return False to continue testing
    
    async def _initial_build(self) -> bool:
        """
        Build and deploy the app for the first time.
        NOW WITH PROACTIVE RESEARCH PHASE!
        """
        print(f"\n{'='*70}")
        print(f"🔨 INITIAL BUILD (WITH RESEARCH)")
        print(f"{'='*70}\n")
        
        goal = """Build a friend chat web app:
        1. Flask backend (app.py) with /chat endpoint
        2. HTML template (templates/index.html) with chat interface
        3. CSS (static/style.css) with modern design
        4. JavaScript (static/script.js) for chat functionality
        5. requirements.txt with Flask dependency"""
        
        # 🔬 RESEARCH PHASE: Learn about the topic BEFORE building
        print("🔬 PHASE 1: PROACTIVE RESEARCH")
        research = await self.research_agent.research_goal(goal)
        
        # Print what we learned
        print(f"\n✅ Research complete:")
        print(f"   • {len(research['topics'])} topics researched")
        print(f"   • {sum(len(p) for p in research['best_practices'].values())} best practices learned")
        print(f"   • {len(research['pitfalls'])} common pitfalls identified")
        print()
        
        # 🔨 BUILD PHASE: Now build with knowledge
        print("🔨 PHASE 2: BUILDING WITH KNOWLEDGE")
        result = await self.engine.run(goal)
        
        if not result['success']:
            print(f"❌ Build failed")
            return False
            
        print(f"✅ Build complete")
        return self.deploy()
    
    def deploy(self) -> bool:
        """Deploy the Flask app."""
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
        return True
    
    async def _strategy_direct_file_fix(self) -> bool:
        """
        Strategy 1: Direct file fix (file-aware + memory-aware + knowledge-aware)
        NOW checks knowledge base for relevant information!
        """
        print(f"\n💡 STRATEGY: Direct File Fix (Memory + Knowledge + File-Aware)")
        
        error_message = "\n".join(self.last_errors)
        
        # Step 1: Check memory for known solutions
        has_solution, solution_data = self.meta_learner.analyze_error(
            self.last_errors, 
            self._get_files_state()
        )
        
        if has_solution and not solution_data.get('trigger_self_improvement'):
            print(f"🧠 MEMORY: Found known solution!")
            fixed_code = solution_data['solution']['fixed_code']
            file_path = solution_data['solution']['file_path']
            target_file = self.workspace / file_path
            target_file.write_text(fixed_code)
            print(f"✅ Applied known solution to {file_path}")
            return True
        
        # Step 2: Check knowledge base for relevant information
        print(f"📚 KNOWLEDGE BASE: Searching for relevant knowledge...")
        knowledge_results = self.knowledge_base.search_knowledge(error_message)
        
        if knowledge_results:
            print(f"📚 Found {len(knowledge_results)} relevant knowledge entries:")
            for result in knowledge_results[:3]:  # Show top 3
                print(f"   • {result['topic']}")
        
        # Step 3: Determine which file needs fixing
        file_path, file_content = self._detect_problem_file(error_message)
        
        if not file_path:
            print("❌ Could not determine which file to fix")
            return False
        
        # Step 4: Generate fix (with knowledge context)
        fixed_code = await self._generate_fix_with_knowledge(
            file_path, 
            file_content, 
            error_message,
            knowledge_results
        )
        
        if not fixed_code:
            return False
        
        # Step 5: Apply fix
        target_file = self.workspace / file_path
        target_file.write_text(fixed_code)
        print(f"✅ Applied fix to {file_path}")
        
        # Store as pending (will be saved only if verification succeeds)
        error_signature = self.meta_learner.create_signature_from_error(error_message)
        self.pending_solution = {
            'error_signature': error_signature,
            'fixed_code': fixed_code,
            'file_path': file_path
        }
        
        return True
    
    async def _strategy_contextual_file_fix(self) -> bool:
        """
        Strategy 2: Contextual file fix
        Provides multiple related files to LLM for better context.
        """
        print(f"\n💡 STRATEGY: Contextual File Fix (Multiple Files)")
        
        error_message = "\n".join(self.last_errors)
        file_path, file_content = self._detect_problem_file(error_message)
        
        if not file_path:
            return False
        
        # Get related files for context
        context_files = self._get_related_files(file_path)
        context_str = "\n".join([f"File: {f}\n{(self.workspace / f).read_text()}\n" 
                                 for f in context_files if (self.workspace / f).exists()])
        
        # Enhanced prompt with context
        prompt = f"""Fix the following error with full project context:

ERROR:
{error_message}

MAIN FILE TO FIX ({file_path}):
{file_content}

RELATED FILES FOR CONTEXT:
{context_str}

Generate the COMPLETE, CORRECTED version of {file_path}:"""
        
        fixed_code = await self._llm_call(prompt)
        
        if not fixed_code:
            return False
        
        target_file = self.workspace / file_path
        target_file.write_text(fixed_code)
        print(f"✅ Applied contextual fix to {file_path}")
        
        return True
    
    async def _strategy_use_template(self) -> bool:
        """
        Strategy 3: Use proven template
        Instead of generating, FORCEFULLY apply a known working template.
        This strategy NEVER asks Gemini - it just copies the proven code.
        """
        print(f"\n💡 STRATEGY: Use Proven Template (FORCEFUL)")
        
        error_message = "\n".join(self.last_errors)
        error_lower = error_message.lower()
        
        # HTML/Frontend issues - use proven HTML template
        if any(kw in error_lower for kw in [
            "missing", "chat-container", "message-form", 
            "javascript", "dom", "selector", "element"
        ]):
            print("🎯 Detected frontend error - applying COMPLETE proven template set")
            
            # Apply proven HTML
            html_path = self.workspace / "templates" / "index.html"
            html_path.parent.mkdir(exist_ok=True, parents=True)
            html_path.write_text(self.html_template)
            print(f"✅ Applied proven HTML: templates/index.html")
            
            # Also ensure we have basic CSS
            css_path = self.workspace / "static" / "style.css"
            css_path.parent.mkdir(exist_ok=True, parents=True)
            if not css_path.exists() or len(css_path.read_text()) < 100:
                css_path.write_text("""
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background: #f0f0f0;
}
#chat-container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
#messages {
    min-height: 300px;
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 20px;
}
#message-form {
    display: flex;
    gap: 10px;
}
#message-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
button {
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background: #0056b3;
}
""")
                print(f"✅ Applied proven CSS: static/style.css")
            
            # Also ensure we have basic JS
            js_path = self.workspace / "static" / "script.js"
            if not js_path.exists() or len(js_path.read_text()) < 100:
                js_path.write_text("""
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('message-form');
    const input = document.getElementById('message-input');
    const messages = document.getElementById('messages');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        // Display user message
        messages.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
        input.value = '';

        // Send to backend
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            });
            const data = await response.json();
            messages.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
            messages.scrollTop = messages.scrollHeight;
        } catch (error) {
            messages.innerHTML += `<div style="color: red;">Error: ${error.message}</div>`;
        }
    });
});
""")
                print(f"✅ Applied proven JS: static/script.js")
            
            return True
        
        print("⚠️ Template strategy not applicable to this error type")
        return False
    
    async def _strategy_web_search(self) -> bool:
        """
        Strategy 4: Web-assisted learning
        Search the web for solutions when all else fails.
        """
        print(f"\n💡 STRATEGY: Web-Assisted Learning")
        
        error_message = "\n".join(self.last_errors)
        file_path, file_content = self._detect_problem_file(error_message)
        
        if not file_path:
            return False
        
        # Call WebLearner
        solution = await self.web_learner.search_for_solution(
            error_message=error_message,
            tech_stack=["Python", "Flask", "Playwright"],
            current_file_content=file_content,
            current_file_path=file_path
        )
        
        if not solution:
            print("❌ Web search did not find a solution")
            return False
        
        print(f"🌐 Solution found from: {solution['source_url']}")
        
        # Apply the web-learned solution
        target_file = self.workspace / file_path
        target_file.write_text(solution['fixed_code'])
        print(f"✅ Applied web-learned solution to {file_path}")
        
        return True
    
    def _detect_problem_file(self, error_message: str) -> Tuple[Optional[str], Optional[str]]:
        """Determines which file needs to be fixed based on error."""
        error_lower = error_message.lower()
        
        # HTML issues
        if any(kw in error_lower for kw in ["selector", "#chat-container", "#message-form", "missing:", "dom", "element"]):
            file_path = "templates/index.html"
        # CSS issues
        elif any(kw in error_lower for kw in ["css", "style", "stylesheet"]):
            file_path = "static/style.css"
        # JS issues
        elif any(kw in error_lower for kw in ["javascript", "js error", "script.js"]):
            file_path = "static/script.js"
        # Requirements issues
        elif "requirements.txt" in error_lower or "file is empty or too small" in error_lower:
            file_path = "requirements.txt"
        # Default to Python backend
        else:
            file_path = "app.py"
        
        target_file = self.workspace / file_path
        if not target_file.exists():
            return None, None
        
        print(f"🎯 Detected problem in: {file_path}")
        return file_path, target_file.read_text()
    
    def _get_related_files(self, file_path: str) -> List[str]:
        """Get files related to the target file for context."""
        if "templates" in file_path:
            return ["static/style.css", "static/script.js", "app.py"]
        elif "static" in file_path:
            return ["templates/index.html", "app.py"]
        elif "app.py" in file_path:
            return ["templates/index.html", "requirements.txt"]
        return []
    
    def _get_files_state(self) -> Dict:
        """Get current state of all files (for meta-learner)."""
        files = {}
        for file_path in ["app.py", "templates/index.html", "static/style.css", "static/script.js", "requirements.txt"]:
            full_path = self.workspace / file_path
            if full_path.exists():
                files[file_path] = {
                    'size': len(full_path.read_text()),
                    'exists': True
                }
        return files
    
    async def _generate_fix(self, file_path: str, file_content: str, error_message: str) -> Optional[str]:
        """Generate a fix using LLM (without knowledge context)."""
        prompt = f"""Fix the following error in {file_path}:

ERROR:
{error_message}

CURRENT CODE:
{file_content}

Generate the COMPLETE, CORRECTED version of {file_path}:"""
        
        return await self._llm_call(prompt)
    
    async def _generate_fix_with_knowledge(
        self, 
        file_path: str, 
        file_content: str, 
        error_message: str,
        knowledge_results: List[Dict]
    ) -> Optional[str]:
        """Generate a fix using LLM WITH knowledge base context."""
        
        # Build knowledge context
        knowledge_context = ""
        if knowledge_results:
            knowledge_context = "\n**RELEVANT KNOWLEDGE FROM RESEARCH:**\n"
            for result in knowledge_results[:3]:  # Top 3 results
                knowledge_context += f"\nTopic: {result['topic']}\n"
                if 'entries' in result:
                    for entry in result['entries'][-2:]:  # Last 2 entries
                        knowledge_context += f"- {entry['knowledge']}\n"
                elif 'entry' in result:
                    knowledge_context += f"- {result['entry']['knowledge']}\n"
        
        prompt = f"""Fix the following error in {file_path}:

ERROR:
{error_message}

CURRENT CODE:
{file_content}
{knowledge_context}

**YOUR TASK:**
Using the knowledge above and best practices, generate the COMPLETE, CORRECTED version of {file_path}.

OUTPUT ONLY THE COMPLETE, CORRECTED CODE (no explanations):"""
        
        return await self._llm_call(prompt)
    
    async def _llm_call(self, prompt: str) -> Optional[str]:
        """Make an LLM call via ResilientLLM."""
        try:
            response = await self.llm.generate_fix(prompt)
            
            # Remove markdown if present
            code = response.strip()
            if code.startswith("```"):
                lines = code.split("\n")
                code = "\n".join(lines[1:-1])
            
            return code
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            return None


async def main():
    """Run the cognitive autonomous system with continuous learning."""
    workspace_dir = "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/autonomous_engine/friend_chat_app"
    
    print("\n" + "="*70)
    print("🧠 META APP BUILDER V3.0 - PHASE 2.10")
    print("CONTINUOUS LEARNING SYSTEM")
    print("="*70)
    print("\nThis system will:")
    print("  • 🔬 Research topics BEFORE building (proactive)")
    print("  • 📚 Build and reference a knowledge base")
    print("  • 🧠 Remember what works (memory)")
    print("  • 💡 Try different strategies when stuck")
    print("  • 🌐 Search the web for real solutions")
    print("  • ✨ Never repeat the same mistake")
    print("="*70 + "\n")
    
    # Create the executor
    builder = MetaAppBuilderV3(workspace_dir=workspace_dir)
    
    # Create the cognitive supervisor
    supervisor = CognitiveSupervisor(executor=builder)
    
    # Run the autonomous flow
    success = await supervisor.run_autonomous_flow()
    
    if success:
        print("\n" + "="*70)
        print("🎉 APPLICATION IS FULLY OPERATIONAL!")
        print("="*70)
        print(f"\n🌐 Access your app at: http://localhost:{builder.port}")
        print("\nThe app will continue running. Press Ctrl+C to stop.")
        
        # Keep the app running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
            if builder.server_process:
                builder.server_process.terminate()
    else:
        print("\n" + "="*70)
        print("❌ COULD NOT ACHIEVE FULL FUNCTIONALITY")
        print("="*70)
        print("\nThe system tried all available strategies.")
        print("Manual intervention may be required.")


if __name__ == "__main__":
    asyncio.run(main())

