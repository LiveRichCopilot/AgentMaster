"""
Code Executor Tool for JAi
Allows JAi to run Python code and see the actual results.
"""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any


def execute_python_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute Python code and return the output.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        dict: Execution results with stdout, stderr, and exit code
    """
    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute the code
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Clean up
        os.unlink(temp_file)
        
        success = result.returncode == 0
        
        return {
            'status': 'success' if success else 'error',
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'output': result.stdout if success else result.stderr
        }
        
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {
            'status': 'error',
            'error': f'Code execution timed out after {timeout} seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to execute code: {str(e)}'
        }


def read_file_content(filepath: str, tool_context = None) -> Dict[str, Any]:
    """
    Read a file and return its contents.
    
    Args:
        filepath: Path to the file to read
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: File contents and metadata
    """
    try:
        path = Path(filepath)
        
        if not path.exists():
            return {
                'status': 'error',
                'error': f'File not found: {filepath}'
            }
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'status': 'success',
            'filepath': str(path.absolute()),
            'content': content,
            'size_bytes': len(content),
            'lines': len(content.split('\n'))
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to read file: {str(e)}'
        }

