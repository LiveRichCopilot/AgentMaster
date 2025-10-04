"""
Environment Tools - File System and Command Execution
Gives the autonomous agent the ability to interact with the real environment.

Phase 1: Basic File and Command Operations
- Create, read, update files
- Execute shell commands
- Capture and interpret results
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import json


class EnvironmentTools:
    """
    Provides tools for the autonomous agent to interact with the environment.
    
    Safety Features:
    - Working directory constraint (agent can only work in designated folder)
    - Command validation (prevent dangerous commands)
    - Error handling and logging
    """
    
    def __init__(self, workspace_dir: str):
        """
        Initialize environment tools with a workspace directory.
        
        Args:
            workspace_dir: Directory where agent can create/modify files
        """
        self.workspace_dir = Path(workspace_dir).resolve()
        
        # Create workspace if it doesn't exist
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔧 Environment tools initialized")
        print(f"📁 Workspace: {self.workspace_dir}")
        
        # Track all operations for auditing
        self.operations_log = []
        
    def _is_safe_path(self, filepath: str) -> bool:
        """Check if a path is within the workspace directory."""
        resolved_path = (self.workspace_dir / filepath).resolve()
        try:
            resolved_path.relative_to(self.workspace_dir)
            return True
        except ValueError:
            return False
            
    def _log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        """Log an operation for auditing."""
        from datetime import datetime
        log_entry = {
            'operation': operation,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.operations_log.append(log_entry)
        
    def create_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """
        Create a new file in the workspace.
        
        Args:
            filepath: Relative path within workspace
            content: File contents
            
        Returns:
            dict: Status and result information
        """
        try:
            # Security check
            if not self._is_safe_path(filepath):
                return {
                    'success': False,
                    'error': f'Path {filepath} is outside workspace'
                }
                
            full_path = self.workspace_dir / filepath
            
            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self._log_operation('create_file', {'filepath': filepath, 'size': len(content)})
            
            print(f"📄 Created file: {filepath}")
            
            return {
                'success': True,
                'filepath': str(full_path),
                'size_bytes': len(content),
                'message': f'File created: {filepath}'
            }
            
        except Exception as e:
            error_msg = f"Failed to create file {filepath}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """
        Read a file from the workspace.
        
        Args:
            filepath: Relative path within workspace
            
        Returns:
            dict: File contents and metadata
        """
        try:
            if not self._is_safe_path(filepath):
                return {
                    'success': False,
                    'error': f'Path {filepath} is outside workspace'
                }
                
            full_path = self.workspace_dir / filepath
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {filepath}'
                }
                
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self._log_operation('read_file', {'filepath': filepath})
            
            return {
                'success': True,
                'filepath': str(full_path),
                'content': content,
                'size_bytes': len(content),
                'lines': len(content.split('\n'))
            }
            
        except Exception as e:
            error_msg = f"Failed to read file {filepath}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    def update_file(self, filepath: str, new_content: str) -> Dict[str, Any]:
        """
        Update an existing file.
        
        Args:
            filepath: Relative path within workspace
            new_content: New file contents
            
        Returns:
            dict: Status and result information
        """
        try:
            if not self._is_safe_path(filepath):
                return {
                    'success': False,
                    'error': f'Path {filepath} is outside workspace'
                }
                
            full_path = self.workspace_dir / filepath
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {filepath}'
                }
                
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            self._log_operation('update_file', {'filepath': filepath, 'new_size': len(new_content)})
            
            print(f"✏️  Updated file: {filepath}")
            
            return {
                'success': True,
                'filepath': str(full_path),
                'size_bytes': len(new_content),
                'message': f'File updated: {filepath}'
            }
            
        except Exception as e:
            error_msg = f"Failed to update file {filepath}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    def list_files(self, directory: str = ".") -> Dict[str, Any]:
        """
        List files in a directory within the workspace.
        
        Args:
            directory: Relative path to directory (default: root of workspace)
            
        Returns:
            dict: List of files and directories
        """
        try:
            if not self._is_safe_path(directory):
                return {
                    'success': False,
                    'error': f'Path {directory} is outside workspace'
                }
                
            full_path = self.workspace_dir / directory
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'Directory not found: {directory}'
                }
                
            files = []
            directories = []
            
            for item in full_path.iterdir():
                if item.is_file():
                    files.append(item.name)
                elif item.is_dir():
                    directories.append(item.name)
                    
            return {
                'success': True,
                'directory': str(full_path),
                'files': sorted(files),
                'directories': sorted(directories),
                'total_items': len(files) + len(directories)
            }
            
        except Exception as e:
            error_msg = f"Failed to list directory {directory}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    def run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute a shell command in the workspace directory.
        
        Args:
            command: Shell command to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            dict: Command output and exit code
        """
        try:
            # Basic security: prevent some dangerous commands
            dangerous_commands = ['rm -rf /', 'sudo', 'mkfs', 'dd if=']
            if any(cmd in command.lower() for cmd in dangerous_commands):
                return {
                    'success': False,
                    'error': f'Command blocked for safety: {command}'
                }
                
            print(f"⚙️  Running command: {command}")
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            
            self._log_operation('run_command', {
                'command': command,
                'exit_code': result.returncode,
                'success': success
            })
            
            if success:
                print(f"✅ Command succeeded")
            else:
                print(f"⚠️  Command failed with exit code {result.returncode}")
            
            return {
                'success': success,
                'command': command,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout}s: {command}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Failed to run command: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
            
    def get_operations_log(self) -> list:
        """Get the log of all operations performed."""
        return self.operations_log
        
    def save_operations_log(self, filepath: str = "operations.json") -> None:
        """Save the operations log to a file."""
        log_path = self.workspace_dir / filepath
        with open(log_path, 'w') as f:
            json.dump(self.operations_log, f, indent=2)
        print(f"📋 Operations log saved to {filepath}")

