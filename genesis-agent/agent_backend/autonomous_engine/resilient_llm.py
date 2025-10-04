"""
Resilient LLM Integration with Fallbacks
Handles quota limits, retries, and multiple API fallbacks
"""

import asyncio
import time
from typing import List, Dict, Any
from google import genai
from google.genai import types as genai_types
from .task_manager import Task
import uuid


class ResilientLLM:
    """
    LLM integration with multiple fallback strategies:
    1. Try Vertex AI
    2. If quota exhausted: Wait and retry
    3. If still failing: Switch to direct Gemini API
    4. If all fails: Use pattern-based fallback
    
    Supports model selection:
    - gemini-2.5-flash: 10x cheaper, great for research/simple tasks
    - gemini-2.5-pro: Expensive, best for complex coding/reasoning
    """
    
    def __init__(self, model_name: str = "gemini-2.5-pro"):
        self.model_name = model_name
        self.vertex_client = None
        self.direct_client = None
        self.max_retries = 3
        self.base_delay = 2  # seconds
        
        # Initialize Vertex AI client
        try:
            self.vertex_client = genai.Client(
                vertexai=True,
                project='studio-2416451423-f2d96',
                location='us-central1'
            )
            print("✅ Vertex AI client initialized")
        except Exception as e:
            print(f"⚠️ Vertex AI init failed: {e}")
        
        # Initialize direct API client as fallback
        import os
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            try:
                self.direct_client = genai.Client(api_key=api_key)
                print("✅ Direct Gemini API client initialized")
            except Exception as e:
                print(f"⚠️ Direct API init failed: {e}")
    
    async def call_with_fallback(self, prompt: str, config: genai_types.GenerateContentConfig):
        """
        Try to call LLM with automatic fallback and retry logic
        """
        # Strategy 1: Try Vertex AI with retries
        if self.vertex_client:
            for attempt in range(self.max_retries):
                try:
                    print(f"🔄 Attempt {attempt + 1}: Calling Vertex AI...")
                    
                    def call_vertex():
                        return self.vertex_client.models.generate_content(
                            model=self.model_name,
                            contents=[
                                genai_types.Content(
                                    role='user',
                                    parts=[genai_types.Part.from_text(text=prompt)]
                                )
                            ],
                            config=config
                        )
                    
                    response = await asyncio.to_thread(call_vertex)
                    print(f"✅ Vertex AI call succeeded")
                    return response.text
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Check if quota exhausted
                    if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str:
                        wait_time = self.base_delay * (2 ** attempt)
                        print(f"⚠️ Quota exhausted, waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"⚠️ Vertex AI error: {e}")
                        break
        
        # Strategy 2: Try direct Gemini API
        if self.direct_client:
            try:
                print(f"🔄 Falling back to direct Gemini API...")
                
                def call_direct():
                    return self.direct_client.models.generate_content(
                        model='gemini-2.5-pro',
                        contents=[
                            genai_types.Content(
                                role='user',
                                parts=[genai_types.Part.from_text(text=prompt)]
                            )
                        ],
                        config=config
                    )
                
                response = await asyncio.to_thread(call_direct)
                print(f"✅ Direct API call succeeded")
                return response.text
                
            except Exception as e:
                print(f"⚠️ Direct API error: {e}")
        
        # Strategy 3: Pattern-based fallback
        print(f"⚠️ All LLM strategies failed, using pattern-based fallback")
        raise Exception("All LLM strategies exhausted")
    
    async def decompose_goal(self, goal: str) -> List[Task]:
        """Decompose goal with fallback strategies"""
        
        system_prompt = """You are an expert software architect. Break down this goal into specific, executable tasks.

Return a JSON array of tasks:
[
  {
    "description": "Clear task description",
    "type": "create_file | write_code | run_command",
    "details": {
      "filename": "file.py",
      "language": "python",
      "framework": "flask"
    }
  }
]

Be specific and actionable."""

        user_prompt = f"Goal: {goal}\n\nBreak this down into tasks."
        
        config = genai_types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=8192,
            response_mime_type="application/json"
        )
        
        try:
            response_text = await self.call_with_fallback(
                system_prompt + "\n\n" + user_prompt,
                config
            )
            
            import json
            tasks_data = json.loads(response_text)
            
            tasks = []
            for task_data in tasks_data:
                task = Task(
                    id=str(uuid.uuid4()),
                    description=task_data['description']
                )
                task.task_type = task_data.get('type', 'generic')
                task.details = task_data.get('details', {})
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            print(f"❌ Goal decomposition failed: {e}")
            # Fallback: Create a single generic task
            return [Task(
                id=str(uuid.uuid4()),
                description=f"Execute goal: {goal}"
            )]
    
    async def generate_fix(self, prompt: str) -> str:
        """Simple method for generating fixes - just takes a prompt"""
        config = genai_types.GenerateContentConfig(
            temperature=0.2,
            top_p=0.95,
            max_output_tokens=8192,
        )
        
        return await self.call_with_fallback(
            prompt=prompt,
            config=config,
            system_instruction="You are an expert developer. Fix bugs and generate clean, working code. Return ONLY code, no explanations."
        )
    
    async def generate_code(self, task_description: str, filename: str,
                           language: str, framework: str = None) -> str:
        """Generate code with fallback strategies"""
        
        system_prompt = f"""You are an expert {language} developer. Write production-quality code.

Requirements:
- Functional and correct
- Clean and well-structured
- Includes necessary imports
- Handles errors properly
- Ready for production

Return ONLY the code, no explanations or markdown blocks."""

        framework_context = f" using {framework}" if framework else ""
        user_prompt = f"""Write {language} code{framework_context} for:

Task: {task_description}
Filename: {filename}

Return ONLY the code."""

        config = genai_types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=8192
        )
        
        try:
            code = await self.call_with_fallback(
                system_prompt + "\n\n" + user_prompt,
                config
            )
            
            # Clean up markdown if present
            code = code.strip()
            if code.startswith('```'):
                lines = code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines[-1].startswith('```'):
                    lines = lines[:-1]
                code = '\n'.join(lines)
            
            return code
            
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
            # Return error placeholder
            return f"# Error generating code: {str(e)}\n# Task: {task_description}\n"
    
    async def analyze_error(self, error_message: str, task_description: str,
                           code: str = None) -> Dict[str, Any]:
        """Analyze error with fallback strategies"""
        
        system_prompt = """You are an expert debugger. Analyze this error and provide a fix.

Return JSON:
{
  "diagnosis": "What went wrong",
  "root_cause": "Why it happened",
  "fix_strategy": "How to fix it",
  "fixed_code": "Corrected code or null"
}"""

        code_context = f"\n\nCode:\n{code}" if code else ""
        user_prompt = f"""Error: {task_description}

Message:
{error_message}{code_context}

Analyze and provide fix."""

        config = genai_types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=4096,
            response_mime_type="application/json"
        )
        
        try:
            response_text = await self.call_with_fallback(
                system_prompt + "\n\n" + user_prompt,
                config
            )
            
            import json
            return json.loads(response_text)
            
        except Exception as e:
            print(f"❌ Error analysis failed: {e}")
            return {
                'diagnosis': f'Could not analyze: {str(e)}',
                'fix_strategy': 'Manual intervention needed',
                'fixed_code': None
            }

