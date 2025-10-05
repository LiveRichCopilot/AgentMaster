"""
WORKFLOW TOOLS - Tool Orchestration Layer

These tools combine multiple atomic tools into intelligent workflows.
Instead of the agent choosing between 116 tools, it calls ONE workflow tool
that automatically executes the right sequence.

This solves decision paralysis and ensures critical steps (like validation) never get skipped.
"""

from google.adk.tools import ToolContext
import logging

logger = logging.getLogger(__name__)


def smart_deploy_workflow(
    service_name: str,
    source_directory: str,
    tool_context: ToolContext
) -> dict:
    """INTELLIGENT DEPLOYMENT WORKFLOW - Instructions for proper deployment.
    
    This tool provides the CORRECT SEQUENCE for deployment with validation.
    
    Instead of the agent manually choosing tools and potentially skipping validation,
    this returns the exact workflow to follow.
    
    Args:
        service_name: Name of Cloud Run service
        source_directory: Path to source code
    
    Returns:
        dict with workflow instructions
    """
    
    return {
        'status': 'workflow_instructions',
        'service_name': service_name,
        'source_directory': source_directory,
        'workflow': [
            {
                'step': 1,
                'action': 'verify_before_deploy',
                'description': 'Check source code for issues before deploying',
                'required': True
            },
            {
                'step': 2,
                'action': 'Transfer to CloudExpert',
                'description': 'CloudExpert has deploy_to_cloud_run tool',
                'required': True
            },
            {
                'step': 3,
                'action': 'validate_deployment_success',
                'description': 'CRITICAL - Test the deployed URL to verify it actually works',
                'required': True,
                'warning': 'NEVER SKIP THIS STEP - Do not claim success without validation'
            },
            {
                'step': 4,
                'action': 'debug_deployment_failure (if validation fails)',
                'description': 'If validation shows broken app, auto-diagnose the issue',
                'required': 'conditional'
            }
        ],
        'message': f'To deploy {service_name}, follow this workflow. Transfer to CloudExpert for deployment, then VALIDATE the result.',
        'critical_reminder': 'NEVER say "deployment successful" until step 3 (validation) confirms it actually works'
    }


def smart_debug_workflow(
    service_name: str,
    error_description: str,
    tool_context: ToolContext
) -> dict:
    """INTELLIGENT DEBUG WORKFLOW - Instructions for proper debugging.
    
    Instead of agent choosing between 6 debug tools randomly,
    this returns the correct sequence to diagnose issues.
    
    Args:
        service_name: Name of failing Cloud Run service
        error_description: What's broken (user description or error message)
    
    Returns:
        dict with debugging workflow instructions
    """
    
    return {
        'status': 'workflow_instructions',
        'service_name': service_name,
        'error_description': error_description,
        'workflow': [
            {
                'step': 1,
                'action': 'parse_cloud_run_error',
                'description': 'Parse the error message to identify error type',
                'required': True
            },
            {
                'step': 2,
                'action': 'get_cloud_run_logs',
                'description': 'Fetch actual logs from Cloud Run to see real errors',
                'required': True
            },
            {
                'step': 3,
                'action': 'analyze_failure_pattern',
                'description': 'Look for patterns in repeated failures',
                'required': True
            },
            {
                'step': 4,
                'action': 'debug_deployment_failure',
                'description': 'Full diagnosis with root cause and recommended fix',
                'required': True
            }
        ],
        'message': f'To debug {service_name}, follow this workflow. Transfer to CloudExpert who has all debug tools.',
        'critical_reminder': 'Do not guess at fixes - follow the workflow to see actual errors first'
    }


def smart_analyze_workflow(
    content_path: str,
    content_type: str,
    analysis_goal: str,
    tool_context: ToolContext
) -> dict:
    """INTELLIGENT ANALYSIS WORKFLOW - Instructions for proper analysis.
    
    Instead of agent choosing between multiple analysis tools randomly,
    this returns the correct sequence based on content type.
    
    Args:
        content_path: Path to file or URL
        content_type: "image", "video", "code", "github_repo"
        analysis_goal: What user wants ("extract design", "find bugs", "transcribe")
    
    Returns:
        dict with analysis workflow instructions
    """
    
    workflows = {
        'image': [
            {'step': 1, 'action': 'analyze_image', 'description': 'Basic image analysis'},
            {'step': 2, 'action': 'extract_design_system (if design-related)', 'description': 'Extract colors, fonts, spacing'}
        ],
        'video': [
            {'step': 1, 'action': 'transcribe_video', 'description': 'Transcribe audio to text'},
            {'step': 2, 'action': 'analyze_video', 'description': 'Visual content analysis'}
        ],
        'github_repo': [
            {'step': 1, 'action': 'Transfer to CodeMaster', 'description': 'CodeMaster has analyze_github_repo tool'}
        ],
        'code': [
            {'step': 1, 'action': 'Transfer to CodeMaster', 'description': 'CodeMaster has lint_python_code and analyze_code_complexity tools'}
        ]
    }
    
    workflow = workflows.get(content_type, [
        {'step': 1, 'action': 'Determine content type first', 'description': 'Unknown content type'}
    ])
    
    return {
        'status': 'workflow_instructions',
        'content_path': content_path,
        'content_type': content_type,
        'analysis_goal': analysis_goal,
        'workflow': workflow,
        'message': f'To analyze {content_type}, follow this workflow',
        'critical_reminder': 'Transfer to specialist agents (CodeMaster) for code analysis'
    }


def select_relevant_tools(
    task_description: str,
    tool_context: ToolContext
) -> dict:
    """INTELLIGENT TOOL SELECTOR - Narrows 116 tools to 5-10 relevant ones.
    
    Takes user's request and returns ONLY the tools needed for that task.
    This prevents decision paralysis from having 116 choices.
    
    Args:
        task_description: What the user wants to do
    
    Returns:
        dict with 'relevant_tools' (list of 5-10 tool names) and 'reasoning'
    """
    
    task_lower = task_description.lower()
    relevant_tools = []
    reasoning = []
    
    # Deployment tasks
    if any(word in task_lower for word in ['deploy', 'cloud run', 'publish', 'launch']):
        relevant_tools.extend([
            'smart_deploy_workflow',  # Use workflow instead of individual tools
            'list_directory',
            'find_directory',
            'read_file_content'
        ])
        reasoning.append("Deployment task detected - using smart_deploy_workflow")
    
    # Debugging tasks
    if any(word in task_lower for word in ['debug', 'error', 'broken', 'not working', 'failed']):
        relevant_tools.extend([
            'smart_debug_workflow',  # Use workflow instead of individual tools
            'get_cloud_run_logs',
            'get_cloud_build_logs',
            'describe_cloud_run_service'
        ])
        reasoning.append("Debugging task detected - using smart_debug_workflow")
    
    # Analysis tasks
    if any(word in task_lower for word in ['analyze', 'image', 'video', 'github', 'code']):
        relevant_tools.extend([
            'smart_analyze_workflow',  # Use workflow instead of individual tools
            'analyze_image',
            'analyze_video',
            'analyze_github_repo'
        ])
        reasoning.append("Analysis task detected - using smart_analyze_workflow")
    
    # Design/UI tasks
    if any(word in task_lower for word in ['design', 'ui', 'component', 'css', 'tailwind']):
        relevant_tools.extend([
            'extract_design_system',
            'generate_apple_ui_component',
            'generate_css_styles',
            'setup_tailwind_css'
        ])
        reasoning.append("Design task detected")
    
    # Memory/context tasks
    if any(word in task_lower for word in ['remember', 'recall', 'context', 'project', 'notes']):
        relevant_tools.extend([
            'remember_project_context',
            'recall_project_context',
            'update_project_notes',
            'search_memory'
        ])
        reasoning.append("Memory task detected")
    
    # Cloud infrastructure tasks
    if any(word in task_lower for word in ['iam', 'permission', 'secret', 'firestore', 'storage']):
        relevant_tools.extend([
            'grant_iam_permission',
            'check_iam_permissions',
            'create_secret',
            'get_secret',
            'check_firestore_database',
            'check_cloud_storage_buckets'
        ])
        reasoning.append("Cloud infrastructure task detected")
    
    # Remove duplicates
    relevant_tools = list(set(relevant_tools))
    
    # If no specific category matched, return general-purpose tools
    if not relevant_tools:
        relevant_tools = [
            'simple_search',
            'read_file_content',
            'list_directory',
            'remember_project_context',
            'recall_project_context'
        ]
        reasoning.append("General task - using core tools")
    
    return {
        'status': 'success',
        'task': task_description,
        'relevant_tools': relevant_tools[:10],  # Max 10 tools
        'reasoning': reasoning,
        'message': f"Narrowed from 116 tools to {len(relevant_tools)} relevant tools"
    }
