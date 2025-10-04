"""
LLM Integration for Autonomous Engine
Phase 2: Adds Gemini 2.5 Pro intelligence to the autonomous execution loop
"""

import os
import json
from typing import List, Dict, Any
from google import genai
from google.genai import types as genai_types
from .task_manager import Task
import uuid


class LLMIntegration:
    """
    Integrates Gemini 2.5 Pro for intelligent autonomous execution.
    
    Capabilities:
    - Intelligent goal decomposition
    - Code generation
    - Error analysis and self-correction
    """
    
    def __init__(self, use_vertex_ai: bool = True):
        """
        Initialize the LLM integration.
        
        Args:
            use_vertex_ai: Whether to use Vertex AI (True) or direct API key (False)
        """
        # Initialize Gemini client
        if use_vertex_ai:
            # Use Vertex AI (same as JAi Cortex)
            self.client = genai.Client(
                vertexai=True,
                project='studio-2416451423-f2d96',
                location='us-central1'
            )
            print("🧠 LLM Integration initialized (Gemini 2.5 Pro via Vertex AI)")
        else:
            # Use direct API key
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            self.client = genai.Client(api_key=api_key)
            print("🧠 LLM Integration initialized (Gemini 2.5 Pro via API Key)")
        
        # Model configuration for autonomous execution
        self.model_config = genai_types.GenerateContentConfig(
            temperature=0.3,  # Lower for more consistent code generation
            max_output_tokens=8192,
            response_mime_type="application/json"  # Structured output
        )
        
    async def decompose_goal(self, goal: str) -> List[Task]:
        """
        Use Gemini to intelligently break down a high-level goal into tasks.
        
        Args:
            goal: High-level goal from user
            
        Returns:
            List of Task objects to execute
        """
        
        # EXCELLENT SYSTEM PROMPT for goal decomposition
        system_prompt = """You are an expert software architect and project planner for an autonomous code execution system.

Your role: Break down high-level goals into specific, executable tasks.

Requirements for each task:
1. SPECIFIC - Clear, actionable description
2. EXECUTABLE - Can be accomplished by file operations or code generation
3. ORDERED - Logical dependency order
4. COMPLETE - All necessary steps included

Task Types Available:
- create_file: Create a new file
- write_code: Generate code for a file
- run_command: Execute a shell command
- verify_result: Check if previous task succeeded

Guidelines:
- Start with file creation, then add content
- Include tests if code is being written
- Add verification steps for critical tasks
- Keep tasks atomic (one clear purpose each)
- Think about dependencies (what needs to happen first)

Output Format:
Return a JSON array of tasks, each with:
{
  "description": "Clear description of what to do",
  "type": "create_file | write_code | run_command | verify_result",
  "details": {
    "filename": "name of file (if applicable)",
    "language": "programming language (if code)",
    "framework": "framework/library (if applicable)",
    "command": "shell command (if run_command)"
  }
}

Example:
Goal: "Create a React button component with tests"
Output:
[
  {
    "description": "Create Button component file",
    "type": "create_file",
    "details": {"filename": "Button.tsx", "language": "typescript"}
  },
  {
    "description": "Write React Button component with props and styling",
    "type": "write_code",
    "details": {"filename": "Button.tsx", "language": "typescript", "framework": "react"}
  },
  {
    "description": "Create test file for Button component",
    "type": "create_file", 
    "details": {"filename": "Button.test.tsx", "language": "typescript"}
  },
  {
    "description": "Write comprehensive tests for Button component",
    "type": "write_code",
    "details": {"filename": "Button.test.tsx", "language": "typescript", "framework": "react-testing-library"}
  }
]

Be thorough but efficient. Quality over quantity."""

        user_prompt = f"""Goal: {goal}

Break this down into specific, executable tasks following the guidelines above."""

        try:
            # Call Gemini (wrapped in to_thread because it's a blocking call)
            import asyncio
            
            def call_gemini():
                return self.client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=[
                        genai_types.Content(
                            role='user',
                            parts=[genai_types.Part.from_text(text=system_prompt + "\n\n" + user_prompt)]
                        )
                    ],
                    config=self.model_config
                )
            
            response = await asyncio.to_thread(call_gemini)
            
            # Parse response
            tasks_data = json.loads(response.text)
            
            # Convert to Task objects
            tasks = []
            for task_data in tasks_data:
                task = Task(
                    id=str(uuid.uuid4()),
                    description=task_data['description']
                )
                # Store task type and details for execution
                task.task_type = task_data.get('type', 'generic')
                task.details = task_data.get('details', {})
                tasks.append(task)
            
            print(f"🎯 Gemini decomposed goal into {len(tasks)} tasks")
            return tasks
            
        except Exception as e:
            print(f"❌ Error in goal decomposition: {e}")
            # Fallback to simple task
            return [Task(
                id=str(uuid.uuid4()),
                description=f"Execute goal: {goal}"
            )]
    
    async def generate_code(self, task_description: str, filename: str, 
                           language: str, framework: str = None) -> str:
        """
        Use Gemini to generate actual production-quality code.
        
        Args:
            task_description: What the code should do
            filename: Target filename
            language: Programming language
            framework: Optional framework/library
            
        Returns:
            Generated code as string
        """
        
        # EXCELLENT SYSTEM PROMPT for code generation
        system_prompt = """You are an expert software engineer writing production-quality code.

Your code must be:
1. FUNCTIONAL - Works correctly and handles edge cases
2. CLEAN - Follows best practices and style guides
3. DOCUMENTED - Includes helpful comments for complex logic
4. TESTED - Ready for testing (write testable code)
5. MODERN - Uses current patterns and APIs

Requirements:
- Include all necessary imports
- Add proper error handling
- Use type hints (TypeScript, Python)
- Follow naming conventions
- Make it production-ready

Critical Rules:
- Return ONLY the code, no explanations or markdown
- Do NOT wrap code in ```language``` blocks
- Do NOT add "Here's the code:" or similar text
- Just pure, clean code ready to save to a file

Example Output for React Component:
import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export default function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button 
      onClick={onClick}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
}

That's it. Clean, pure code."""

        framework_context = f" using {framework}" if framework else ""
        
        user_prompt = f"""Write {language} code{framework_context} for:

Task: {task_description}
Filename: {filename}

Remember: Return ONLY the code, nothing else."""

        try:
            # Call Gemini for code generation (wrapped in to_thread because it's blocking)
            import asyncio
            
            def call_gemini():
                return self.client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=[
                        genai_types.Content(
                            role='user',
                            parts=[genai_types.Part.from_text(text=system_prompt + "\n\n" + user_prompt)]
                        )
                    ],
                    config=genai_types.GenerateContentConfig(
                        temperature=0.2,  # Very low for consistent code
                        max_output_tokens=8192,
                    )
                )
            
            response = await asyncio.to_thread(call_gemini)
            
            code = response.text.strip()
            
            # Clean up any markdown that might have slipped through
            if code.startswith('```'):
                # Remove markdown code blocks
                lines = code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines[-1].startswith('```'):
                    lines = lines[:-1]
                code = '\n'.join(lines)
            
            print(f"💻 Generated {len(code)} chars of {language} code")
            return code
            
        except Exception as e:
            print(f"❌ Error generating code: {e}")
            # Return placeholder
            return f"// Error generating code: {str(e)}\n// Task: {task_description}\n"
    
    async def analyze_error(self, error_message: str, task_description: str, 
                           code: str = None) -> Dict[str, Any]:
        """
        Use Gemini to analyze an error and suggest fixes.
        
        Args:
            error_message: The error that occurred
            task_description: What we were trying to do
            code: The code that failed (if applicable)
            
        Returns:
            dict with 'diagnosis', 'fix_strategy', and 'fixed_code' (if applicable)
        """
        
        # EXCELLENT SYSTEM PROMPT for error analysis
        system_prompt = """You are an expert debugging specialist.

Your role: Analyze errors and provide clear, actionable fixes.

Analysis Format:
{
  "diagnosis": "Clear explanation of what went wrong and why",
  "root_cause": "The underlying issue",
  "fix_strategy": "Step-by-step plan to fix it",
  "fixed_code": "Corrected code (if error was in code, otherwise null)",
  "prevention": "How to prevent this error in future"
}

Be concise but thorough. Focus on the actual fix."""

        code_context = f"\n\nCode that failed:\n{code}" if code else ""
        
        user_prompt = f"""Error occurred while: {task_description}

Error message:
{error_message}{code_context}

Analyze this error and provide a fix."""

        try:
            # Call Gemini for error analysis (wrapped in to_thread because it's blocking)
            import asyncio
            
            def call_gemini():
                return self.client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=[
                        genai_types.Content(
                            role='user',
                            parts=[genai_types.Part.from_text(text=system_prompt + "\n\n" + user_prompt)]
                        )
                    ],
                    config=genai_types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=4096,
                        response_mime_type="application/json"
                    )
                )
            
            response = await asyncio.to_thread(call_gemini)
            
            analysis = json.loads(response.text)
            print(f"🔍 Error analyzed: {analysis.get('root_cause', 'Unknown')}")
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing error: {e}")
            return {
                'diagnosis': f'Could not analyze error: {str(e)}',
                'fix_strategy': 'Manual intervention required',
                'fixed_code': None
            }

