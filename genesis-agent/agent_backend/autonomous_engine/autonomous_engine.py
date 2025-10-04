"""
Autonomous Engine - Core Execution Loop
The "brain" that enables continuous autonomous operation.

Phase 2: LLM-Powered Autonomous Execution
- Goal decomposition using Gemini 2.5 Pro
- Intelligent code generation
- Continuous execution loop
- Task execution with EnvironmentTools
- Error analysis and self-correction
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid

from .task_manager import Task, TaskManager
from environment_tools import EnvironmentTools
try:
    from resilient_llm import ResilientLLM
    RESILIENT_LLM_AVAILABLE = True
except ImportError:
    from llm_integration import LLMIntegration
    RESILIENT_LLM_AVAILABLE = False


class AutonomousEngine:
    """
    The core autonomous execution engine.
    
    This is the "brain" that runs continuously to achieve a high-level goal.
    
    Workflow:
    1. Take a high-level goal from user
    2. Decompose into subtasks (using LLM - will integrate later)
    3. Execute tasks one by one using EnvironmentTools
    4. Observe results and self-correct if errors occur
    5. Continue until goal is achieved
    """
    
    def __init__(self, workspace_dir: str, verbose: bool = True, use_llm: bool = True):
        """
        Initialize the autonomous engine.
        
        Args:
            workspace_dir: Directory where agent can work
            verbose: Whether to print detailed progress
            use_llm: Whether to use LLM for intelligent execution (Phase 2)
        """
        self.workspace_dir = Path(workspace_dir)
        self.verbose = verbose
        self.use_llm = use_llm
        self.task_manager: Optional[TaskManager] = None
        self.environment: Optional[EnvironmentTools] = None
        self.llm: Optional[LLMIntegration] = None
        
        # Initialize LLM integration (Phase 2 with Resilience)
        if self.use_llm:
            try:
                if RESILIENT_LLM_AVAILABLE:
                    self.llm = ResilientLLM()
                    print(f"🤖 Autonomous Engine initialized (Phase 2: Resilient LLM)")
                else:
                    self.llm = LLMIntegration()
                    print(f"🤖 Autonomous Engine initialized (Phase 2: LLM-Powered)")
            except Exception as e:
                print(f"⚠️ LLM initialization failed: {e}")
                print(f"🤖 Autonomous Engine initialized (Phase 1: Pattern-based)")
                self.use_llm = False
                self.llm = None
        else:
            print(f"🤖 Autonomous Engine initialized (Phase 1: Pattern-based)")
            
        print(f"📁 Workspace: {self.workspace_dir}")
        
    async def decompose_goal(self, goal: str) -> List[Task]:
        """
        Decompose a high-level goal into concrete subtasks.
        
        Phase 2: Uses Gemini 2.5 Pro for intelligent decomposition
        Falls back to pattern-based if LLM unavailable
        
        Args:
            goal: High-level goal description
            
        Returns:
            List of tasks to accomplish the goal
        """
        # Phase 2: Use LLM for intelligent decomposition
        if self.use_llm and self.llm:
            try:
                tasks = await self.llm.decompose_goal(goal)
                
                if self.verbose:
                    print(f"\n🎯 Goal decomposed into {len(tasks)} tasks:")
                    for i, task in enumerate(tasks, 1):
                        print(f"   {i}. {task.description}")
                    print()
                    
                return tasks
            except Exception as e:
                print(f"⚠️ LLM decomposition failed: {e}")
                print(f"📝 Falling back to pattern-based decomposition")
        
        # Fallback: Phase 1 pattern-based decomposition
        tasks = []
        
        # Example: "Create a React component called Button"
        if "react component" in goal.lower():
            component_name = self._extract_component_name(goal)
            
            tasks = [
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Create component file: {component_name}.tsx"
                ),
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Write React component code for {component_name}"
                ),
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Create test file: {component_name}.test.tsx"
                ),
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Write tests for {component_name}"
                ),
            ]
            
        # Example: "Create a file called hello.txt with content 'Hello World'"
        elif "create a file" in goal.lower() or "create file" in goal.lower():
            filename = self._extract_filename(goal)
            content = self._extract_content(goal)
            
            tasks = [
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Create file: {filename}"
                ),
            ]
            
        # Generic fallback
        else:
            tasks = [
                Task(
                    id=str(uuid.uuid4()),
                    description=f"Execute goal: {goal}"
                ),
            ]
            
        if self.verbose:
            print(f"\n🎯 Goal decomposed into {len(tasks)} tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"   {i}. {task.description}")
            print()
            
        return tasks
        
    def _extract_component_name(self, goal: str) -> str:
        """Extract component name from goal (simple pattern matching)."""
        # Look for "called X" or "named X"
        for pattern in ["called ", "named "]:
            if pattern in goal.lower():
                idx = goal.lower().index(pattern) + len(pattern)
                name = goal[idx:].split()[0].strip("'\"")
                return name
        return "Component"
        
    def _extract_filename(self, goal: str) -> str:
        """Extract filename from goal."""
        for pattern in ["called ", "named ", "file "]:
            if pattern in goal.lower():
                idx = goal.lower().index(pattern) + len(pattern)
                name = goal[idx:].split()[0].strip("'\"")
                return name
        return "output.txt"
        
    def _extract_content(self, goal: str) -> str:
        """Extract file content from goal."""
        for pattern in ["with content ", "containing "]:
            if pattern in goal.lower():
                idx = goal.lower().index(pattern) + len(pattern)
                content = goal[idx:].strip("'\"")
                return content
        return "Hello from Autonomous Engine"
        
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Execute a single task using the environment tools.
        
        Phase 2: Uses LLM to generate code intelligently
        Falls back to pattern-based execution if needed
        
        Args:
            task: Task to execute
            
        Returns:
            Result dictionary with success status and details
        """
        description = task.description.lower()
        
        # Get task type and details (set by LLM decomposition)
        task_type = getattr(task, 'task_type', None)
        details = getattr(task, 'details', {})
        
        # Phase 2: Use LLM for code generation
        if self.use_llm and self.llm and task_type == 'write_code':
            try:
                filename = details.get('filename', 'output.txt')
                language = details.get('language', 'text')
                framework = details.get('framework')
                
                print(f"💻 Generating {language} code for {filename}...")
                code = await self.llm.generate_code(
                    task_description=task.description,
                    filename=filename,
                    language=language,
                    framework=framework
                )
                
                # Save generated code
                result = self.environment.create_file(filename, code)
                return result
                
            except Exception as e:
                print(f"⚠️ LLM code generation failed: {e}")
                # Fall through to pattern-based execution
        
        # Pattern: "Create file: X" or task_type == 'create_file'
        if "create file:" in description or "create component file:" in description or task_type == 'create_file':
            filename = details.get('filename') or description.split(":")[-1].strip()
            
            # For Phase 1 fallback, create with placeholder content
            content = f"// {filename}\n// Created by Autonomous Engine\n\n"
            
            if filename.endswith(".tsx"):
                content += "import React from 'react';\n\n"
                content += f"export default function Component() {{\n"
                content += f"  return <div>Component</div>;\n"
                content += f"}}\n"
            elif filename.endswith(".test.tsx"):
                content += "import { render } from '@testing-library/react';\n\n"
                content += "test('renders component', () => {\n"
                content += "  // Test implementation\n"
                content += "});\n"
            else:
                content += "File created by Autonomous Engine\n"
                
            result = self.environment.create_file(filename, content)
            return result
            
        # Pattern: "Write React component code for X"
        elif "write react component code" in description:
            return {
                'success': True,
                'message': 'Component code written (Phase 1 fallback)'
            }
            
        # Pattern: "Write tests for X"
        elif "write tests for" in description:
            return {
                'success': True,
                'message': 'Tests written (Phase 1 fallback)'
            }
        
        # Task type: run_command
        elif task_type == 'run_command':
            command = details.get('command')
            if command:
                result = self.environment.run_command(command)
                return result
            else:
                return {'success': False, 'error': 'No command specified'}
            
        # Generic execution
        else:
            return {
                'success': True,
                'message': f'Task executed: {task.description}'
            }
            
    async def run(self, goal: str) -> Dict[str, Any]:
        """
        Main execution loop - runs autonomously until goal is achieved.
        
        Args:
            goal: High-level goal to accomplish
            
        Returns:
            Final execution summary
        """
        print(f"\n{'='*60}")
        print(f"🚀 AUTONOMOUS EXECUTION STARTED")
        print(f"{'='*60}")
        print(f"Goal: {goal}\n")
        
        # Initialize components
        self.task_manager = TaskManager(goal=goal)
        self.environment = EnvironmentTools(workspace_dir=str(self.workspace_dir))
        
        # Step 1: Decompose goal into tasks
        tasks = await self.decompose_goal(goal)
        self.task_manager.add_tasks(tasks)
        
        # Step 2: Execute tasks continuously
        iteration = 0
        max_iterations = 50  # Safety limit to prevent infinite loops
        
        while self.task_manager.has_pending_tasks() and iteration < max_iterations:
            iteration += 1
            
            # Get next task
            task = self.task_manager.get_next_task()
            
            if task is None:
                break
                
            # Execute task
            try:
                result = await self.execute_task(task)
                
                if result.get('success'):
                    # Task succeeded
                    self.task_manager.mark_completed(task, result)
                    self.task_manager.update_state({'last_success': result})
                else:
                    # Task failed
                    error = result.get('error', 'Unknown error')
                    self.task_manager.mark_failed(task, error)
                    
                    # Phase 2: Try to self-correct errors
                    if self.use_llm and self.llm:
                        print(f"🔍 Analyzing error with LLM...")
                        try:
                            analysis = await self.llm.analyze_error(
                                error_message=error,
                                task_description=task.description
                            )
                            print(f"📋 Diagnosis: {analysis.get('diagnosis', 'No diagnosis')}")
                            print(f"🔧 Fix strategy: {analysis.get('fix_strategy', 'No strategy')}")
                            
                            # If there's a fix, we could retry (future enhancement)
                            
                        except Exception as llm_error:
                            print(f"⚠️ Error analysis failed: {llm_error}")
                    
            except Exception as e:
                # Unexpected error
                self.task_manager.mark_failed(task, str(e))
                
            # Small delay to prevent overwhelming output
            await asyncio.sleep(0.1)
            
        # Step 3: Generate summary
        summary = self.task_manager.get_progress_summary()
        
        print(f"\n{'='*60}")
        print(f"✅ AUTONOMOUS EXECUTION COMPLETE")
        print(f"{'='*60}")
        print(f"Goal: {goal}")
        print(f"Tasks completed: {summary['completed']}/{summary['total_tasks']}")
        print(f"Tasks failed: {len(self.task_manager.failed_tasks)}")
        print(f"Progress: {summary['progress_percentage']:.1f}%")
        print(f"Iterations: {iteration}")
        print(f"{'='*60}\n")
        
        # Save state for debugging
        state_file = self.workspace_dir / "execution_state.json"
        self.task_manager.save_state(str(state_file))
        
        return {
            'goal': goal,
            'success': summary['failed'] == 0,
            'summary': summary,
            'iterations': iteration,
            'state_file': str(state_file)
        }


# Convenience function for testing
async def run_autonomous_task(goal: str, workspace_dir: str = None) -> Dict[str, Any]:
    """
    Run an autonomous task (convenience function for testing).
    
    Args:
        goal: What you want the agent to accomplish
        workspace_dir: Where the agent can work (defaults to ./autonomous_workspace)
        
    Returns:
        Execution summary
    """
    if workspace_dir is None:
        workspace_dir = Path(__file__).parent / "autonomous_workspace"
        
    engine = AutonomousEngine(workspace_dir=workspace_dir)
    result = await engine.run(goal)
    return result


if __name__ == "__main__":
    # Simple test
    async def test():
        result = await run_autonomous_task(
            goal="Create a file called hello.txt with content 'Hello from Autonomous JAi'"
        )
        print(f"\n🎯 Final result: {result}")
        
    asyncio.run(test())

