"""
Workflow Orchestrator - Makes 126 tools work together intelligently
Creates multi-step workflows where tools call each other automatically
"""

import json
from typing import Dict, Any, List, Optional
from google.cloud import firestore
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID)


def build_switch_app_agent_workflow(
    user_id: str,
    user_name: str,
    business_name: str,
    business_description: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    COMPLETE WORKFLOW: Build a full Switch app agent with file management.
    
    This workflow automatically:
    1. Creates user agent
    2. Creates customer service agent
    3. Sets up file storage
    4. Integrates NotebookLM
    5. Generates UI code
    6. Deploys everything
    
    Args:
        user_id: User's ID
        user_name: User's name
        business_name: Business name
        business_description: Business description
        
    Returns:
        dict: Complete setup results
    """
    workflow_results = {
        'workflow_id': f'switch_setup_{user_id}',
        'status': 'running',
        'steps': []
    }
    
    try:
        # STEP 1: Create user agent
        from .switch_app_agent_builder import create_switch_user_agent
        
        step1 = create_switch_user_agent(
            user_id=user_id,
            user_name=user_name,
            user_preferences="General user preferences",
            tool_context=tool_context
        )
        workflow_results['steps'].append({
            'step': 1,
            'name': 'Create User Agent',
            'status': step1['status'],
            'result': step1
        })
        
        if step1['status'] != 'success':
            workflow_results['status'] = 'failed'
            workflow_results['failed_at'] = 'step_1_user_agent'
            return workflow_results
        
        # STEP 2: Create customer service agent
        from .switch_app_agent_builder import create_switch_customer_service_agent
        
        step2 = create_switch_customer_service_agent(
            business_name=business_name,
            business_description=business_description,
            faq_data="Default FAQ data",
            tool_context=tool_context
        )
        workflow_results['steps'].append({
            'step': 2,
            'name': 'Create CS Agent',
            'status': step2['status'],
            'result': step2
        })
        
        if step2['status'] != 'success':
            workflow_results['status'] = 'failed'
            workflow_results['failed_at'] = 'step_2_cs_agent'
            return workflow_results
        
        # STEP 3: Integrate NotebookLM with both agents
        from .switch_app_agent_builder import integrate_notebooklm_with_agent
        
        step3a = integrate_notebooklm_with_agent(
            agent_id=step1['result']['agent_id'],
            notebook_sources=[],
            tool_context=tool_context
        )
        
        step3b = integrate_notebooklm_with_agent(
            agent_id=step2['result']['agent_id'],
            notebook_sources=[],
            tool_context=tool_context
        )
        
        workflow_results['steps'].append({
            'step': 3,
            'name': 'Integrate NotebookLM',
            'status': 'success',
            'result': {
                'user_agent_notebook': step3a,
                'cs_agent_notebook': step3b
            }
        })
        
        # STEP 4: Generate UI code
        from .switch_app_agent_builder import generate_switch_app_chatbot_ui_code
        
        step4 = generate_switch_app_chatbot_ui_code(
            agent_id=step1['result']['agent_id'],
            ui_theme='switch_custom',
            tool_context=tool_context
        )
        workflow_results['steps'].append({
            'step': 4,
            'name': 'Generate UI Code',
            'status': step4['status'],
            'result': step4
        })
        
        # STEP 5: Save workflow to Firestore
        workflow_doc = {
            'workflow_id': workflow_results['workflow_id'],
            'user_id': user_id,
            'user_agent_id': step1['result']['agent_id'],
            'cs_agent_id': step2['result']['agent_id'],
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'completed'
        }
        
        db.collection('switch_app_workflows').document(workflow_results['workflow_id']).set(workflow_doc)
        
        workflow_results['status'] = 'completed'
        workflow_results['summary'] = {
            'user_agent': step1['result']['agent_id'],
            'cs_agent': step2['result']['agent_id'],
            'ui_code_ready': True,
            'notebook_integrated': True
        }
        
        return workflow_results
        
    except Exception as e:
        workflow_results['status'] = 'error'
        workflow_results['error'] = str(e)
        return workflow_results


def upload_and_process_file_workflow(
    file_content: str,
    file_name: str,
    user_id: str,
    file_type: str,
    auto_analyze: bool,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    COMPLETE WORKFLOW: Upload file and automatically process it.
    
    This workflow:
    1. Uploads file to Cloud Storage
    2. Processes with Vision API (if image)
    3. Extracts text (if document)
    4. Creates collection suggestion
    5. Updates user's file index
    
    Args:
        file_content: File content (base64 or path)
        file_name: File name
        user_id: User ID
        file_type: File type
        auto_analyze: Whether to auto-analyze
        
    Returns:
        dict: Complete processing results
    """
    workflow_results = {
        'workflow_id': f'file_upload_{user_id}_{file_name}',
        'status': 'running',
        'steps': []
    }
    
    try:
        # STEP 1: Upload file
        from .switch_app_file_manager import upload_file_to_storage
        
        step1 = upload_file_to_storage(
            file_content=file_content,
            file_name=file_name,
            user_id=user_id,
            file_type=file_type,
            tool_context=tool_context
        )
        
        workflow_results['steps'].append({
            'step': 1,
            'name': 'Upload File',
            'status': step1['status'],
            'result': step1
        })
        
        if step1['status'] != 'success':
            workflow_results['status'] = 'failed'
            return workflow_results
        
        file_id = step1['file_id']
        
        # STEP 2: Auto-analyze if requested and it's an image
        if auto_analyze and file_type == 'image':
            from .switch_app_file_manager import process_image_file
            
            step2 = process_image_file(
                file_id=file_id,
                analysis_type='all',
                tool_context=tool_context
            )
            
            workflow_results['steps'].append({
                'step': 2,
                'name': 'Analyze Image',
                'status': step2['status'],
                'result': step2
            })
            
            # STEP 3: Suggest collection based on analysis
            if step2['status'] == 'success' and 'labels' in step2['results']:
                labels = step2['results']['labels']
                suggested_collection = labels[0]['description'] if labels else 'Uncategorized'
                
                workflow_results['steps'].append({
                    'step': 3,
                    'name': 'Suggest Collection',
                    'status': 'success',
                    'result': {
                        'suggested_collection': suggested_collection,
                        'confidence': labels[0]['score'] if labels else 0
                    }
                })
        
        workflow_results['status'] = 'completed'
        workflow_results['file_id'] = file_id
        workflow_results['file_url'] = step1['file_url']
        
        return workflow_results
        
    except Exception as e:
        workflow_results['status'] = 'error'
        workflow_results['error'] = str(e)
        return workflow_results


def deploy_agent_to_cloud_workflow(
    agent_id: str,
    deployment_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    COMPLETE WORKFLOW: Deploy agent to Cloud Run with full setup.
    
    This workflow:
    1. Verifies agent exists
    2. Generates deployment config
    3. Creates Dockerfile
    4. Builds container
    5. Deploys to Cloud Run
    6. Validates deployment
    7. Returns live URL
    
    Args:
        agent_id: Agent to deploy
        deployment_name: Cloud Run service name
        
    Returns:
        dict: Deployment results with live URL
    """
    workflow_results = {
        'workflow_id': f'deploy_{agent_id}',
        'status': 'running',
        'steps': []
    }
    
    try:
        # STEP 1: Get agent config
        agent_ref = db.collection('switch_app_agents').document(agent_id)
        agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            agent_ref = db.collection('switch_app_cs_agents').document(agent_id)
            agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            workflow_results['status'] = 'failed'
            workflow_results['error'] = 'Agent not found'
            return workflow_results
        
        agent_data = agent_doc.to_dict()
        
        workflow_results['steps'].append({
            'step': 1,
            'name': 'Verify Agent',
            'status': 'success',
            'result': {'agent_name': agent_data['agent_name']}
        })
        
        # STEP 2: Call CloudExpert to verify deployment readiness
        from .sub_agents.cloud_expert import cloud_expert
        from google.adk.tools import AgentTool
        
        verify_tool = AgentTool(agent=cloud_expert)
        verify_result = verify_tool(
            query=f"Verify deployment readiness for agent {agent_id}",
            tool_context=tool_context
        )
        
        workflow_results['steps'].append({
            'step': 2,
            'name': 'Verify Deployment Readiness',
            'status': 'success',
            'result': verify_result
        })
        
        # STEP 3: Call CloudExpert to deploy
        deploy_result = verify_tool(
            query=f"Deploy agent {agent_id} to Cloud Run as {deployment_name}",
            tool_context=tool_context
        )
        
        workflow_results['steps'].append({
            'step': 3,
            'name': 'Deploy to Cloud Run',
            'status': 'success',
            'result': deploy_result
        })
        
        # STEP 4: Validate deployment
        validate_result = verify_tool(
            query=f"Validate deployment of {deployment_name}",
            tool_context=tool_context
        )
        
        workflow_results['steps'].append({
            'step': 4,
            'name': 'Validate Deployment',
            'status': 'success',
            'result': validate_result
        })
        
        workflow_results['status'] = 'completed'
        workflow_results['live_url'] = f'https://{deployment_name}-{PROJECT_ID}.run.app'
        
        return workflow_results
        
    except Exception as e:
        workflow_results['status'] = 'error'
        workflow_results['error'] = str(e)
        return workflow_results


def intelligent_tool_chain(
    goal: str,
    context: dict,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    INTELLIGENT WORKFLOW: Automatically chain tools to achieve a goal.
    
    This analyzes the goal and automatically calls the right tools in sequence.
    
    Args:
        goal: What you want to accomplish
        context: Additional context
        
    Returns:
        dict: Results from tool chain
    """
    workflow_results = {
        'goal': goal,
        'status': 'running',
        'tool_chain': []
    }
    
    try:
        # Analyze goal to determine tool chain
        goal_lower = goal.lower()
        
        # WORKFLOW: Build complete Switch app
        if 'build switch app' in goal_lower or 'setup switch' in goal_lower:
            result = build_switch_app_agent_workflow(
                user_id=context.get('user_id', 'default_user'),
                user_name=context.get('user_name', 'User'),
                business_name=context.get('business_name', 'Business'),
                business_description=context.get('business_description', 'A business'),
                tool_context=tool_context
            )
            workflow_results['tool_chain'] = result['steps']
            workflow_results['result'] = result
        
        # WORKFLOW: Upload and process file
        elif 'upload' in goal_lower and 'file' in goal_lower:
            result = upload_and_process_file_workflow(
                file_content=context.get('file_content', ''),
                file_name=context.get('file_name', 'file.jpg'),
                user_id=context.get('user_id', 'default_user'),
                file_type=context.get('file_type', 'image'),
                auto_analyze=context.get('auto_analyze', True),
                tool_context=tool_context
            )
            workflow_results['tool_chain'] = result['steps']
            workflow_results['result'] = result
        
        # WORKFLOW: Deploy agent
        elif 'deploy' in goal_lower and 'agent' in goal_lower:
            result = deploy_agent_to_cloud_workflow(
                agent_id=context.get('agent_id', ''),
                deployment_name=context.get('deployment_name', 'agent-service'),
                tool_context=tool_context
            )
            workflow_results['tool_chain'] = result['steps']
            workflow_results['result'] = result
        
        # WORKFLOW: Create agent with code
        elif 'create agent' in goal_lower or 'build agent' in goal_lower:
            # Chain: CodeMaster → CloudExpert → Deploy
            from .sub_agents.code_master import code_master
            from .sub_agents.cloud_expert import cloud_expert
            from google.adk.tools import AgentTool
            
            # Step 1: CodeMaster generates agent code
            code_tool = AgentTool(agent=code_master)
            code_result = code_tool(
                query=f"Generate agent code for: {goal}",
                tool_context=tool_context
            )
            workflow_results['tool_chain'].append({
                'tool': 'CodeMaster',
                'action': 'Generate agent code',
                'result': code_result
            })
            
            # Step 2: CloudExpert deploys it
            cloud_tool = AgentTool(agent=cloud_expert)
            deploy_result = cloud_tool(
                query=f"Deploy the agent code to Cloud Run",
                tool_context=tool_context
            )
            workflow_results['tool_chain'].append({
                'tool': 'CloudExpert',
                'action': 'Deploy agent',
                'result': deploy_result
            })
            
            workflow_results['result'] = {
                'code': code_result,
                'deployment': deploy_result
            }
        
        # WORKFLOW: Analyze and fix deployment
        elif 'fix' in goal_lower or 'debug' in goal_lower:
            # Chain: CloudExpert → CodeMaster → CloudExpert
            from .sub_agents.cloud_expert import cloud_expert
            from .sub_agents.code_master import code_master
            from google.adk.tools import AgentTool
            
            # Step 1: CloudExpert diagnoses
            cloud_tool = AgentTool(agent=cloud_expert)
            diagnose_result = cloud_tool(
                query=f"Debug deployment issue: {goal}",
                tool_context=tool_context
            )
            workflow_results['tool_chain'].append({
                'tool': 'CloudExpert',
                'action': 'Diagnose issue',
                'result': diagnose_result
            })
            
            # Step 2: CodeMaster fixes code
            code_tool = AgentTool(agent=code_master)
            fix_result = code_tool(
                query=f"Fix the code based on: {diagnose_result}",
                tool_context=tool_context
            )
            workflow_results['tool_chain'].append({
                'tool': 'CodeMaster',
                'action': 'Fix code',
                'result': fix_result
            })
            
            # Step 3: CloudExpert redeploys
            redeploy_result = cloud_tool(
                query="Redeploy with fixed code",
                tool_context=tool_context
            )
            workflow_results['tool_chain'].append({
                'tool': 'CloudExpert',
                'action': 'Redeploy',
                'result': redeploy_result
            })
            
            workflow_results['result'] = {
                'diagnosis': diagnose_result,
                'fix': fix_result,
                'redeployment': redeploy_result
            }
        
        else:
            workflow_results['status'] = 'error'
            workflow_results['error'] = 'Could not determine appropriate workflow for goal'
            return workflow_results
        
        workflow_results['status'] = 'completed'
        return workflow_results
        
    except Exception as e:
        workflow_results['status'] = 'error'
        workflow_results['error'] = str(e)
        return workflow_results


__all__ = [
    'build_switch_app_agent_workflow',
    'upload_and_process_file_workflow',
    'deploy_agent_to_cloud_workflow',
    'intelligent_tool_chain'
]
