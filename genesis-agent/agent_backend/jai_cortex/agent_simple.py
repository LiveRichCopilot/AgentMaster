"""
JAi Cortex OS - Code Debugging & GitHub Analysis Agent
"""

# MUST import vertex_config FIRST
import vertex_config

import requests
import base64
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types as genai_types
from google.cloud import storage, firestore

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Initialize Cloud clients
db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)

# ============================================================================
# CODE ANALYSIS TOOLS
# ============================================================================

def analyze_code_file(filename: str, code_content: str, issue_description: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Analyze uploaded code files for bugs, errors, and improvements.
    
    Args:
        filename: Name of the file (e.g., 'App.tsx', 'index.js')
        code_content: The actual code content
        issue_description: What problem the user is facing
        
    Returns:
        Analysis with identified issues and fixes
    """
    try:
        # Store in Firestore for reference
        doc_ref = db.collection('code_files').document()
        doc_ref.set({
            'filename': filename,
            'code': code_content,
            'issue': issue_description,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        
        return {
            'status': 'success',
            'message': f'Analyzed {filename}',
            'file_type': filename.split('.')[-1] if '.' in filename else 'unknown',
            'code_length': len(code_content),
            'stored_id': doc_ref.id,
            'analysis': f'Ready to help debug {filename}. I can see {len(code_content)} characters of code.'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def fetch_github_repo(github_url: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Fetch and analyze a GitHub repository.
    
    Args:
        github_url: GitHub repo URL (e.g., https://github.com/user/repo.git)
        
    Returns:
        Repository structure and key files
    """
    try:
        # Extract owner and repo from URL
        # https://github.com/LiveRichCopilot/switch.git
        parts = github_url.replace('.git', '').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        # Fetch repo info from GitHub API
        api_url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return {'status': 'error', 'message': f'Could not fetch repo: {response.status_code}'}
        
        repo_data = response.json()
        
        # Fetch file tree
        tree_url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1'
        tree_response = requests.get(tree_url)
        
        files = []
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            files = [item['path'] for item in tree_data.get('tree', []) if item['type'] == 'blob'][:50]  # First 50 files
        
        return {
            'status': 'success',
            'repo_name': repo_data['name'],
            'description': repo_data.get('description', 'No description'),
            'language': repo_data.get('language', 'Unknown'),
            'stars': repo_data.get('stargazers_count', 0),
            'files_found': len(files),
            'file_list': files,
            'clone_url': repo_data['clone_url'],
            'message': f'Found {len(files)} files in {owner}/{repo}'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def fetch_github_file(github_url: str, file_path: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Fetch a specific file from a GitHub repository.
    
    Args:
        github_url: GitHub repo URL
        file_path: Path to file in repo (e.g., 'src/App.tsx')
        
    Returns:
        File content and metadata
    """
    try:
        parts = github_url.replace('.git', '').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        # Fetch file content
        file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
        response = requests.get(file_url)
        
        if response.status_code != 200:
            return {'status': 'error', 'message': f'File not found: {file_path}'}
        
        file_data = response.json()
        
        # Decode base64 content
        content = base64.b64decode(file_data['content']).decode('utf-8')
        
        return {
            'status': 'success',
            'filename': file_data['name'],
            'path': file_path,
            'size': file_data['size'],
            'content': content,
            'message': f'Fetched {file_path} ({file_data["size"]} bytes)'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def save_debug_note(title: str, content: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Save debugging notes and solutions.
    
    Args:
        title: Title of the note
        content: The note content
        
    Returns:
        Confirmation of saved note
    """
    try:
        doc_ref = db.collection('debug_notes').document()
        doc_ref.set({
            'title': title,
            'content': content,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        
        return {
            'status': 'success',
            'note_id': doc_ref.id,
            'message': f'Saved note: {title}'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

SYSTEM_INSTRUCTION = """You are JAi Cortex OS - an expert code debugging and development assistant.

🎯 **YOUR MISSION:**
Help users debug their code, analyze GitHub repositories, and fix programming issues.

🛠️ **YOUR TOOLS:**

1. **analyze_code_file**: When users paste code or describe a file
   - Ask for: filename, code content, and what's wrong
   - Analyze the code for bugs, errors, and improvements
   - Provide specific fixes

2. **fetch_github_repo**: When users give you a GitHub URL
   - Get the repository structure and file list
   - Tell them what files you found
   - Ask which files they want you to analyze

3. **fetch_github_file**: To get specific files from GitHub
   - Fetch and analyze the actual code
   - Identify issues and suggest fixes

4. **save_debug_note**: Save solutions and debugging notes
   - Keep a record of fixes
   - Store code snippets and solutions

🎨 **HOW TO HELP:**

**When user gives you a GitHub URL:**
1. Use `fetch_github_repo` to see what's in the repo
2. Tell them what files you found
3. Ask which files they want you to look at
4. Use `fetch_github_file` to get specific files
5. Analyze the code and provide debugging help

**When user pastes code:**
1. Ask for filename if not provided
2. Ask what problem they're facing
3. Use `analyze_code_file` to analyze it
4. Provide detailed debugging help

**When you find a solution:**
- Use `save_debug_note` to save it
- Explain the fix clearly
- Provide updated code if needed

💬 **PERSONALITY:**
- Be direct and helpful
- Ask for code/files when needed
- Provide specific, actionable fixes
- Be enthusiastic about solving problems

You're here to make debugging easy and fast!

Current date: 2025-10-01
"""

# Create the agent
root_agent = Agent(
    name="jai_cortex",
    model="gemini-2.5-pro",
    description="Code debugging and GitHub analysis expert",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        analyze_code_file,
        fetch_github_repo,
        fetch_github_file,
        save_debug_note,
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=8192,
    ),
)

__all__ = ['root_agent']
