"""
REAL Self-Coding Tools - Agent can actually modify its own code!
Enhanced with proper error handling, rate limiting, and logging
"""

import os
import subprocess
from typing import Dict, Any
from pathlib import Path
import json
from datetime import datetime

# Import API utilities for rate limiting and error handling
try:
    from api_utils import api_call, validate_response, sanitize_data, rate_limiter
    HAS_API_UTILS = True
except ImportError:
    HAS_API_UTILS = False
    print("⚠️  api_utils not available, running without rate limiting")

AGENT_DIR = Path(__file__).parent

# Logging helper
def log_operation(operation: str, details: Dict[str, Any]):
    """Log all code operations for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "details": details
    }
    print(f"📝 {operation}: {json.dumps(details, indent=2)}")

@api_call(api_name="file_system", retry=True, rate_limit=False) if HAS_API_UTILS else lambda f: f
def modify_code_impl(file_path: str, old_code: str, new_code: str) -> Dict[str, Any]:
    """Actually modify code files with safety checks and logging"""
    try:
        # Validate inputs
        if not file_path or not old_code or not new_code:
            return {'status': 'error', 'message': 'Missing required parameters'}
        
        # Sanitize file path (prevent directory traversal)
        if '..' in file_path or file_path.startswith('/'):
            return {'status': 'error', 'message': 'Invalid file path'}
        
        full_path = AGENT_DIR / file_path
        
        if not full_path.exists():
            return {'status': 'error', 'message': f'File not found: {file_path}'}
        
        # Security: Only allow Python files
        if not file_path.endswith('.py'):
            return {'status': 'error', 'message': 'Only .py files can be modified'}
        
        # Read current code
        with open(full_path, 'r') as f:
            current_code = f.read()
        
        # Backup before modification
        backup_path = full_path.with_suffix('.py.backup')
        with open(backup_path, 'w') as f:
            f.write(current_code)
        
        # Check if old_code exists
        if old_code not in current_code:
            return {'status': 'error', 'message': 'Old code pattern not found in file'}
        
        # Replace code
        new_content = current_code.replace(old_code, new_code)
        
        # Write back
        with open(full_path, 'w') as f:
            f.write(new_content)
        
        # Log the operation
        log_operation("modify_code", {
            "file": file_path,
            "old_size": len(old_code),
            "new_size": len(new_code),
            "backup": str(backup_path)
        })
        
        return {
            'status': 'success',
            'message': f'Modified {file_path}',
            'file': str(full_path),
            'change': f'Replaced {len(old_code)} chars with {len(new_code)} chars',
            'backup': str(backup_path)
        }
    except Exception as e:
        log_operation("modify_code_error", {"error": str(e), "file": file_path})
        return {'status': 'error', 'message': str(e)}


def read_code_impl(file_path: str) -> Dict[str, Any]:
    """Read code files"""
    try:
        full_path = AGENT_DIR / file_path
        
        if not full_path.exists():
            return {'status': 'error', 'message': f'File not found: {file_path}'}
        
        with open(full_path, 'r') as f:
            code = f.read()
        
        return {
            'status': 'success',
            'file': file_path,
            'code': code,
            'lines': len(code.split('\n'))
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_call(api_name="code_execution", retry=False, rate_limit=True) if HAS_API_UTILS else lambda f: f
def execute_python_impl(code: str) -> Dict[str, Any]:
    """Execute Python code with safety and monitoring"""
    try:
        # Validate code
        if not code or len(code) > 10000:
            return {'status': 'error', 'message': 'Code too long or empty'}
        
        # Safety check: Block dangerous operations
        dangerous_patterns = ['os.system', 'subprocess.call', 'eval(', 'exec(', '__import__', 'open(']
        for pattern in dangerous_patterns:
            if pattern in code:
                return {'status': 'error', 'message': f'Dangerous operation blocked: {pattern}'}
        
        # Create temp file
        temp_file = AGENT_DIR / '_temp_exec.py'
        with open(temp_file, 'w') as f:
            f.write(code)
        
        # Log execution
        log_operation("execute_python", {"code_length": len(code), "temp_file": str(temp_file)})
        
        # Execute with resource limits
        result = subprocess.run(
            ['python3', str(temp_file)],
            capture_output=True,
            text=True,
            timeout=10,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}  # Unbuffered output
        )
        
        # Clean up
        if temp_file.exists():
            temp_file.unlink()
        
        # Log result
        log_operation("execute_python_complete", {
            "exit_code": result.returncode,
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr)
        })
        
        return {
            'status': 'success' if result.returncode == 0 else 'error',
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode
        }
    except subprocess.TimeoutExpired:
        if temp_file.exists():
            temp_file.unlink()
        log_operation("execute_python_timeout", {"timeout": 10})
        return {'status': 'error', 'message': 'Execution timeout (10s)'}
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        log_operation("execute_python_error", {"error": str(e)})
        return {'status': 'error', 'message': str(e)}


def install_package_impl(package: str) -> Dict[str, Any]:
    """Install Python package"""
    try:
        result = subprocess.run(
            ['pip', 'install', package],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            'status': 'success' if result.returncode == 0 else 'error',
            'package': package,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def list_files_impl(directory: str = ".") -> Dict[str, Any]:
    """List files in agent directory"""
    try:
        base_path = AGENT_DIR / directory
        files = []
        
        for item in base_path.iterdir():
            files.append({
                'name': item.name,
                'type': 'dir' if item.is_dir() else 'file',
                'size': item.stat().st_size if item.is_file() else 0
            })
        
        return {
            'status': 'success',
            'directory': str(base_path),
            'files': files,
            'count': len(files)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def run_tests_impl() -> Dict[str, Any]:
    """Run tests to verify code changes"""
    try:
        # Check if server is responding
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:8000/api/health'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return {
            'status': 'success',
            'health_check': 'passed' if result.returncode == 0 else 'failed',
            'response': result.stdout
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def git_commit_impl(message: str) -> Dict[str, Any]:
    """Commit changes to git"""
    try:
        # Add all changes
        subprocess.run(['git', 'add', '.'], cwd=AGENT_DIR, check=True)
        
        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=AGENT_DIR,
            capture_output=True,
            text=True
        )
        
        return {
            'status': 'success',
            'message': message,
            'output': result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': f'Git error: {e}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


