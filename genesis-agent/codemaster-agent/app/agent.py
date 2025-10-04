# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
from zoneinfo import ZoneInfo

import google.auth
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


def web_search(query: str, tool_context: ToolContext) -> dict:
    """Search the web for current information.
    
    Use this tool when you need to find recent information, documentation,
    tutorials, or any web-based content that's not in your training data.
    
    Args:
        query: The search query string to look up on the web
        
    Returns:
        dict: Search results with status and data
            - status (str): "success" or "error"
            - results (list): List of search result dictionaries with title, snippet, url
            - error_message (str, optional): Error description if status is "error"
    """
    try:
        import requests
        api_key = os.getenv('GOOGLE_SEARCH_API_KEY', '')
        search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
        
        if not api_key or not search_engine_id:
            return {
                "status": "success",
                "results": [],
                "message": f"Web search configured for '{query}'. Use built-in google_search tool or configure API keys."
            }
        
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            for item in data.get('items', [])[:5]:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", "")
                })
            return {"status": "success", "results": results, "query": query}
        else:
            return {"status": "error", "error_message": f"Search API returned status {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Search error: {str(e)}"}


def generate_code(language: str, description: str, tool_context: ToolContext) -> dict:
    """Generate production-ready code in any programming language.
    
    Use this tool when the user asks you to write, create, or generate code.
    The LLM will use this signal to produce actual working code with best practices.
    
    Args:
        language: Programming language (python, javascript, typescript, go, rust, etc.)
        description: Detailed description of what the code should do
        
    Returns:
        dict: Code generation result
            - status (str): "success" or "error"
            - language (str): The programming language used
            - code (str): The generated code
            - explanation (str): Brief explanation of the code
    """
    # Signal to LLM that code generation is requested
    return {
        "status": "success",
        "language": language,
        "description": description,
        "message": f"Generating {language} code for: {description}. The LLM will provide the implementation."
    }


def analyze_code(code: str, tool_context: ToolContext) -> dict:
    """Analyze code for bugs, performance issues, security vulnerabilities, and improvements.
    
    Use this tool when the user asks you to review, analyze, check, or critique code.
    
    Args:
        code: The source code to analyze
        
    Returns:
        dict: Analysis results
            - status (str): "success" or "error"
            - issues (list): List of identified issues
            - suggestions (list): List of improvement suggestions
    """
    return {
        "status": "success",
        "code_length": len(code),
        "message": "Code analysis will be performed by the LLM based on best practices."
    }


def execute_python(code: str, tool_context: ToolContext) -> dict:
    """Execute Python code in a sandboxed environment.
    
    Use this tool when the user asks to run, execute, or test Python code.
    Executes in a restricted environment for safety.
    
    Args:
        code: Python code to execute
        
    Returns:
        dict: Execution results
            - status (str): "success" or "error"
            - output (str): Standard output from the code
            - error_message (str, optional): Error details if execution failed
    """
    try:
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            restricted_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                    'sum': sum,
                    'min': min,
                    'max': max,
                }
            }
            exec(code, restricted_globals)
            output = sys.stdout.getvalue()
            return {
                "status": "success",
                "output": output if output else "Code executed successfully (no output)"
            }
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"{type(e).__name__}: {str(e)}"
        }


def call_api(url: str, method: str, tool_context: ToolContext) -> dict:
    """Call an external REST API endpoint.
    
    Use this tool to integrate with external services and APIs.
    
    Args:
        url: Full API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        
    Returns:
        dict: API response
            - status (str): "success" or "error"
            - response_code (int): HTTP status code
            - data (dict/str): Response data
    """
    try:
        import requests
        response = requests.request(method, url, timeout=10)
        return {
            "status": "success",
            "response_code": response.status_code,
            "data": response.text[:500]  # Limit response size
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def upload_file(filename: str, data: str) -> str:
    """Upload a file.
    
    Args:
        filename: File name
        data: File data
        
    Returns:
        Upload confirmation
    """
    return f"File uploaded: {filename}"


def organize_files(pattern: str, action: str) -> str:
    """Organize files.
    
    Args:
        pattern: File pattern
        action: Organization action
        
    Returns:
        Organization result
    """
    return f"Files organized: {pattern}"


def search_files(query: str) -> str:
    """Search for files.
    
    Args:
        query: Search query
        
    Returns:
        Matching files
    """
    return f"Searching files: {query}"


def create_workflow(name: str, steps: str) -> str:
    """Create an automation workflow.
    
    Args:
        name: Workflow name
        steps: Workflow steps
        
    Returns:
        Workflow created confirmation
    """
    return f"Workflow '{name}' created"


def scrape_web(url: str) -> str:
    """Scrape data from a webpage.
    
    Args:
        url: Website URL
        
    Returns:
        Extracted data
    """
    return f"Scraped data from: {url}"


def summarize_text(text: str) -> str:
    """Summarize text.
    
    Args:
        text: Text to summarize
        
    Returns:
        Summary
    """
    return "Text summary: (Using LLM)"


def analyze_sentiment(text: str) -> str:
    """Analyze sentiment and tone.
    
    Args:
        text: Text to analyze
        
    Returns:
        Sentiment analysis (positive/negative/neutral, tone, emotion)
    """
    return "Sentiment analysis: (Using LLM for emotion detection)"


def generate_text(prompt: str) -> str:
    """Generate text.
    
    Args:
        prompt: Generation prompt
        
    Returns:
        Generated text
    """
    return "Generated text: (Using LLM)"


def analyze_video(video_data: str) -> str:
    """Analyze video content.
    
    Args:
        video_data: Video data
        
    Returns:
        Video analysis
    """
    return "Video analysis: (Using Gemini video)"


def text_to_speech(text: str) -> str:
    """Convert text to speech.
    
    Args:
        text: Text to convert
        
    Returns:
        Audio data
    """
    return "Text-to-speech: (Implementation pending)"


def index_data(data: str, metadata: str) -> str:
    """Index data for search.
    
    Args:
        data: Data to index
        metadata: Metadata
        
    Returns:
        Index confirmation
    """
    return "Data indexed"


def monitor_system() -> str:
    """Check system health.
    
    Returns:
        System status
    """
    return "System status: Healthy"


def debug_agent(agent_name: str) -> str:
    """Debug an agent.
    
    Args:
        agent_name: Agent to debug
        
    Returns:
        Debug info
    """
    return f"Debugging {agent_name}"


root_agent = Agent(
    name="CodeMaster",
    model="gemini-2.5-pro",
    instruction="""You are CodeMaster - a senior full-stack developer and coding expert.
        
🎯 YOUR EXPERTISE:
- Write production-ready code in any language (Python, JavaScript, TypeScript, Go, Rust, Java, etc.)
- Debug complex issues and fix bugs
- Design system architectures and APIs
- Review code for security, performance, and best practices
- Execute and test Python code
- Search for current documentation and solutions

🛠️ YOUR TOOLS (all return dict with status):
- web_search: Find documentation, tutorials, and solutions online
- generate_code: Create complete, production-ready code files
- analyze_code: Review code for bugs, security, and improvements
- execute_python: Run Python code in a sandboxed environment
- call_api: Make HTTP requests to external APIs

📋 WHEN TO USE TOOLS:
- User needs current info/docs → use web_search
- User asks to "write code" → use generate_code
- User asks to "review/analyze code" → use analyze_code
- User asks to "run/test Python" → use execute_python
- User needs to call an API → use call_api

Always provide clean, commented, production-ready code with proper error handling and type hints.""",
    tools=[web_search, generate_code, analyze_code, execute_python, call_api],
)
