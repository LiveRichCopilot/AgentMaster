"""
Advanced Code Tools - Give agents Cursor-level coding power
Multi-file editing, refactoring, code analysis, and intelligent modifications
"""

import os
import re
import ast
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from google.cloud import firestore
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID)


def read_entire_file(
    file_path: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Read a complete file with line numbers and metadata.
    
    Args:
        file_path: Path to file (absolute or relative)
        
    Returns:
        dict: File contents with metadata
    """
    try:
        # Handle both absolute and relative paths
        if not os.path.isabs(file_path):
            # Try relative to workspace
            workspace_root = "/Users/liverichmedia/Agent master "
            file_path = os.path.join(workspace_root, file_path)
        
        if not os.path.exists(file_path):
            return {
                'status': 'error',
                'message': f'File not found: {file_path}'
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Get file stats
        stats = os.stat(file_path)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'content': content,
            'lines': lines,
            'line_count': len(lines),
            'char_count': len(content),
            'size_bytes': stats.st_size,
            'extension': os.path.splitext(file_path)[1],
            'message': f'Read {len(lines)} lines from {os.path.basename(file_path)}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to read file: {str(e)}'
        }


def edit_file_section(
    file_path: str,
    start_line: int,
    end_line: int,
    new_content: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Edit a specific section of a file (like Cursor's inline edit).
    
    Args:
        file_path: Path to file
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (inclusive)
        new_content: New content to replace the section
        
    Returns:
        dict: Edit result with diff
    """
    try:
        # Read file
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        lines = read_result['lines']
        
        # Validate line numbers
        if start_line < 1 or end_line > len(lines):
            return {
                'status': 'error',
                'message': f'Invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)'
            }
        
        # Store original section for diff
        original_section = '\n'.join(lines[start_line-1:end_line])
        
        # Replace section
        new_lines = new_content.split('\n')
        lines[start_line-1:end_line] = new_lines
        
        # Write back
        new_content_full = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'lines_changed': f'{start_line}-{end_line}',
            'original_line_count': end_line - start_line + 1,
            'new_line_count': len(new_lines),
            'original_section': original_section,
            'new_section': new_content,
            'message': f'Edited lines {start_line}-{end_line} in {os.path.basename(file_path)}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to edit file: {str(e)}'
        }


def search_and_replace_in_file(
    file_path: str,
    search_pattern: str,
    replacement: str,
    use_regex: bool,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Search and replace text in a file (like Cursor's find/replace).
    
    Args:
        file_path: Path to file
        search_pattern: Text or regex to search for
        replacement: Replacement text
        use_regex: Whether to use regex matching
        
    Returns:
        dict: Replace result with match count
    """
    try:
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        content = read_result['content']
        
        # Perform replacement
        if use_regex:
            new_content, count = re.subn(search_pattern, replacement, content)
        else:
            count = content.count(search_pattern)
            new_content = content.replace(search_pattern, replacement)
        
        if count == 0:
            return {
                'status': 'success',
                'file_path': file_path,
                'matches_found': 0,
                'message': 'No matches found'
            }
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'matches_found': count,
            'replacements_made': count,
            'search_pattern': search_pattern,
            'replacement': replacement,
            'message': f'Replaced {count} occurrence(s) in {os.path.basename(file_path)}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to search and replace: {str(e)}'
        }


def insert_code_at_line(
    file_path: str,
    line_number: int,
    code_to_insert: str,
    position: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Insert code at a specific line (before or after).
    
    Args:
        file_path: Path to file
        line_number: Line number to insert at (1-indexed)
        code_to_insert: Code to insert
        position: 'before' or 'after'
        
    Returns:
        dict: Insert result
    """
    try:
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        lines = read_result['lines']
        
        if line_number < 1 or line_number > len(lines):
            return {
                'status': 'error',
                'message': f'Invalid line number: {line_number} (file has {len(lines)} lines)'
            }
        
        # Insert code
        insert_lines = code_to_insert.split('\n')
        
        if position == 'before':
            insert_index = line_number - 1
        elif position == 'after':
            insert_index = line_number
        else:
            return {
                'status': 'error',
                'message': f'Invalid position: {position} (use "before" or "after")'
            }
        
        lines[insert_index:insert_index] = insert_lines
        
        # Write back
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'inserted_at_line': line_number,
            'position': position,
            'lines_inserted': len(insert_lines),
            'message': f'Inserted {len(insert_lines)} line(s) {position} line {line_number}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to insert code: {str(e)}'
        }


def delete_lines_from_file(
    file_path: str,
    start_line: int,
    end_line: int,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Delete specific lines from a file.
    
    Args:
        file_path: Path to file
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (inclusive)
        
    Returns:
        dict: Delete result
    """
    try:
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        lines = read_result['lines']
        
        if start_line < 1 or end_line > len(lines):
            return {
                'status': 'error',
                'message': f'Invalid line range: {start_line}-{end_line}'
            }
        
        # Store deleted content for reference
        deleted_content = '\n'.join(lines[start_line-1:end_line])
        
        # Delete lines
        del lines[start_line-1:end_line]
        
        # Write back
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'deleted_lines': f'{start_line}-{end_line}',
            'lines_deleted': end_line - start_line + 1,
            'deleted_content': deleted_content,
            'message': f'Deleted lines {start_line}-{end_line}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to delete lines: {str(e)}'
        }


def refactor_function_name(
    file_path: str,
    old_function_name: str,
    new_function_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Refactor a function name throughout a file (renames all occurrences).
    
    Args:
        file_path: Path to file
        old_function_name: Current function name
        new_function_name: New function name
        
    Returns:
        dict: Refactor result
    """
    try:
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        content = read_result['content']
        
        # Use regex to match function definitions and calls
        patterns = [
            (rf'\bdef {old_function_name}\b', f'def {new_function_name}'),  # Function definition
            (rf'\b{old_function_name}\(', f'{new_function_name}('),  # Function calls
            (rf'FunctionTool\({old_function_name}\)', f'FunctionTool({new_function_name})'),  # Tool registration
        ]
        
        total_replacements = 0
        new_content = content
        
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, new_content)
            total_replacements += count
        
        if total_replacements == 0:
            return {
                'status': 'success',
                'file_path': file_path,
                'replacements_made': 0,
                'message': f'Function {old_function_name} not found'
            }
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'old_name': old_function_name,
            'new_name': new_function_name,
            'replacements_made': total_replacements,
            'message': f'Refactored {old_function_name} → {new_function_name} ({total_replacements} changes)'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to refactor function: {str(e)}'
        }


def analyze_python_file(
    file_path: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analyze a Python file's structure (functions, classes, imports).
    
    Args:
        file_path: Path to Python file
        
    Returns:
        dict: File analysis with structure
    """
    try:
        read_result = read_entire_file(file_path, tool_context)
        if read_result['status'] != 'success':
            return read_result
        
        content = read_result['content']
        
        # Parse AST
        tree = ast.parse(content)
        
        imports = []
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f'{module}.{alias.name}')
            elif isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                })
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                })
        
        return {
            'status': 'success',
            'file_path': file_path,
            'imports': imports,
            'functions': functions,
            'classes': classes,
            'function_count': len(functions),
            'class_count': len(classes),
            'import_count': len(imports),
            'message': f'Analyzed {os.path.basename(file_path)}: {len(functions)} functions, {len(classes)} classes'
        }
        
    except SyntaxError as e:
        return {
            'status': 'error',
            'message': f'Syntax error in file: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to analyze file: {str(e)}'
        }


def multi_file_search_replace(
    directory: str,
    file_pattern: str,
    search_pattern: str,
    replacement: str,
    use_regex: bool,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Search and replace across multiple files (like Cursor's multi-file edit).
    
    Args:
        directory: Directory to search in
        file_pattern: File pattern (e.g., "*.py", "*.ts")
        search_pattern: Text or regex to search for
        replacement: Replacement text
        use_regex: Whether to use regex
        
    Returns:
        dict: Results for all files
    """
    try:
        # Find matching files
        if not os.path.isabs(directory):
            workspace_root = "/Users/liverichmedia/Agent master "
            directory = os.path.join(workspace_root, directory)
        
        import glob
        pattern = os.path.join(directory, '**', file_pattern)
        files = glob.glob(pattern, recursive=True)
        
        results = []
        total_replacements = 0
        
        for file_path in files:
            if os.path.isfile(file_path):
                result = search_and_replace_in_file(
                    file_path=file_path,
                    search_pattern=search_pattern,
                    replacement=replacement,
                    use_regex=use_regex,
                    tool_context=tool_context
                )
                
                if result['status'] == 'success' and result.get('replacements_made', 0) > 0:
                    results.append(result)
                    total_replacements += result['replacements_made']
        
        return {
            'status': 'success',
            'directory': directory,
            'file_pattern': file_pattern,
            'files_searched': len(files),
            'files_modified': len(results),
            'total_replacements': total_replacements,
            'results': results,
            'message': f'Modified {len(results)} file(s) with {total_replacements} replacement(s)'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed multi-file search/replace: {str(e)}'
        }


def create_new_file_from_template(
    file_path: str,
    template_type: str,
    custom_params: dict,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a new file from a template (Python module, React component, etc.).
    
    Args:
        file_path: Path for new file
        template_type: Type of template (python_module, react_component, api_endpoint, etc.)
        custom_params: Custom parameters for template
        
    Returns:
        dict: Creation result
    """
    try:
        templates = {
            'python_module': '''"""
{description}
"""

from typing import Dict, Any
from google.adk.tools import ToolContext


def {function_name}(
    param1: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    {function_description}
    
    Args:
        param1: Description of param1
        
    Returns:
        dict: Result dictionary
    """
    try:
        # Implementation here
        return {{
            'status': 'success',
            'message': 'Operation completed'
        }}
    except Exception as e:
        return {{
            'status': 'error',
            'message': f'Failed: {{str(e)}}'
        }}


__all__ = ['{function_name}']
''',
            'react_component': '''import React from 'react';

interface {component_name}Props {{
  // Add props here
}}

const {component_name}: React.FC<{component_name}Props> = (props) => {{
  return (
    <div className="{class_name}">
      <h1>{component_name}</h1>
      {/* Component content */}
    </div>
  );
}};

export default {component_name};
''',
            'api_endpoint': '''import {{ NextApiRequest, NextApiResponse }} from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {{
  if (req.method !== 'POST') {{
    return res.status(405).json({{ error: 'Method not allowed' }});
  }}

  try {{
    // API logic here
    return res.status(200).json({{ success: true }});
  }} catch (error) {{
    console.error('API error:', error);
    return res.status(500).json({{ error: 'Internal server error' }});
  }}
}}
'''
        }
        
        if template_type not in templates:
            return {
                'status': 'error',
                'message': f'Unknown template type: {template_type}'
            }
        
        # Fill template
        template = templates[template_type]
        content = template.format(**custom_params)
        
        # Create file
        if not os.path.isabs(file_path):
            workspace_root = "/Users/liverichmedia/Agent master "
            file_path = os.path.join(workspace_root, file_path)
        
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'template_type': template_type,
            'line_count': len(content.split('\n')),
            'message': f'Created {os.path.basename(file_path)} from {template_type} template'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create file: {str(e)}'
        }


__all__ = [
    'read_entire_file',
    'edit_file_section',
    'search_and_replace_in_file',
    'insert_code_at_line',
    'delete_lines_from_file',
    'refactor_function_name',
    'analyze_python_file',
    'multi_file_search_replace',
    'create_new_file_from_template'
]
