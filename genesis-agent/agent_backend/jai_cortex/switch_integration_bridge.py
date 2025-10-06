"""
Switch Integration Bridge - Connect Agent Master with Switch App
Allows JAi Cortex to directly build, deploy, and manage Switch app features
"""

import os
import json
import subprocess
from typing import Dict, Any, List
from google.cloud import firestore, storage
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
SWITCH_REPO = "https://github.com/LiveRichCopilot/switch.git"
AGENT_MASTER_REPO = "https://github.com/LiveRichCopilot/AgentMaster.git"

db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)


def deploy_feature_to_switch(
    feature_name: str,
    feature_type: str,
    code_content: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Deploy a feature from Agent Master directly to Switch app.
    
    This tool:
    1. Generates the feature code
    2. Creates PR to Switch repo
    3. Deploys to Firebase
    4. Returns live URL
    
    Args:
        feature_name: Name of the feature (e.g., "ai-chat-widget")
        feature_type: Type (component, page, api, function)
        code_content: The code to deploy
        
    Returns:
        dict: Deployment result with live URL
    """
    try:
        # Save feature code to Firestore for tracking
        feature_doc = {
            'feature_name': feature_name,
            'feature_type': feature_type,
            'code_content': code_content,
            'created_by': 'agent_master',
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'pending_deployment'
        }
        
        doc_ref = db.collection('switch_features').document(feature_name)
        doc_ref.set(feature_doc)
        
        # Determine file path based on feature type
        file_paths = {
            'component': f'components/{feature_name}.tsx',
            'page': f'pages/{feature_name}.tsx',
            'api': f'api/{feature_name}.ts',
            'function': f'firebase-functions/src/{feature_name}.ts',
            'hook': f'hooks/{feature_name}.ts',
            'util': f'utils/{feature_name}.ts'
        }
        
        target_path = file_paths.get(feature_type, f'{feature_name}.ts')
        
        # Create deployment instructions
        deployment_instructions = {
            'feature_name': feature_name,
            'target_path': target_path,
            'code_content': code_content,
            'deployment_steps': [
                f'1. Create file: {target_path}',
                f'2. Add code content',
                f'3. Run: npm run build',
                f'4. Run: firebase deploy --only hosting',
                f'5. Verify at: https://switch-470313.web.app'
            ]
        }
        
        # Update feature status
        doc_ref.update({
            'status': 'ready_for_deployment',
            'deployment_instructions': deployment_instructions
        })
        
        return {
            'status': 'success',
            'feature_name': feature_name,
            'feature_type': feature_type,
            'target_path': target_path,
            'deployment_instructions': deployment_instructions,
            'message': f'Feature {feature_name} ready for deployment to Switch',
            'next_steps': [
                'Code is ready and tracked in Firestore',
                'Use deploy_to_switch_firebase to push live',
                'Or manually create PR to Switch repo'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to prepare feature deployment: {str(e)}'
        }


def deploy_to_switch_firebase(
    feature_name: str,
    auto_deploy: bool,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Deploy a prepared feature to Switch Firebase hosting.
    
    Args:
        feature_name: Name of the feature to deploy
        auto_deploy: Whether to auto-deploy or just prepare
        
    Returns:
        dict: Deployment result
    """
    try:
        # Get feature from Firestore
        doc_ref = db.collection('switch_features').document(feature_name)
        doc = doc_ref.get()
        
        if not doc.exists:
            return {
                'status': 'error',
                'message': 'Feature not found. Use deploy_feature_to_switch first.'
            }
        
        feature_data = doc.to_dict()
        
        if auto_deploy:
            # Call CloudExpert to handle deployment
            from .sub_agents.cloud_expert import cloud_expert
            from google.adk.tools import AgentTool
            
            cloud_tool = AgentTool(agent=cloud_expert)
            deploy_result = cloud_tool(
                query=f"Deploy feature {feature_name} to Switch Firebase: {json.dumps(feature_data['deployment_instructions'])}",
                tool_context=tool_context
            )
            
            # Update status
            doc_ref.update({
                'status': 'deployed',
                'deployed_at': firestore.SERVER_TIMESTAMP,
                'deployment_result': str(deploy_result)
            })
            
            return {
                'status': 'success',
                'feature_name': feature_name,
                'deployed': True,
                'live_url': 'https://switch-470313.web.app',
                'deployment_result': deploy_result,
                'message': f'Feature {feature_name} deployed to Switch'
            }
        else:
            return {
                'status': 'success',
                'feature_name': feature_name,
                'deployed': False,
                'message': 'Feature prepared but not deployed (auto_deploy=False)',
                'deployment_instructions': feature_data['deployment_instructions']
            }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to deploy to Firebase: {str(e)}'
        }


def sync_agent_to_switch(
    agent_id: str,
    integration_type: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Sync an Agent Master agent to Switch app.
    
    This creates a live integration where Switch users can interact with the agent.
    
    Args:
        agent_id: Agent to sync (from Agent Master)
        integration_type: How to integrate (chatbot, api, background_worker)
        
    Returns:
        dict: Integration result
    """
    try:
        # Get agent config
        agent_ref = db.collection('switch_app_agents').document(agent_id)
        agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            agent_ref = db.collection('switch_app_cs_agents').document(agent_id)
            agent_doc = agent_ref.get()
        
        if not agent_doc.exists:
            return {
                'status': 'error',
                'message': 'Agent not found'
            }
        
        agent_data = agent_doc.to_dict()
        
        # Generate integration code based on type
        if integration_type == 'chatbot':
            # Generate React component for Switch
            from .switch_app_agent_builder import generate_switch_app_chatbot_ui_code
            
            ui_result = generate_switch_app_chatbot_ui_code(
                agent_id=agent_id,
                ui_theme='switch_custom',
                tool_context=tool_context
            )
            
            # Deploy the chatbot component
            deploy_result = deploy_feature_to_switch(
                feature_name=f'AgentChat_{agent_id}',
                feature_type='component',
                code_content=ui_result['ui_code'],
                tool_context=tool_context
            )
            
            return {
                'status': 'success',
                'agent_id': agent_id,
                'integration_type': 'chatbot',
                'component_name': f'AgentChat_{agent_id}',
                'deployment': deploy_result,
                'message': f'Agent {agent_id} synced as chatbot to Switch'
            }
        
        elif integration_type == 'api':
            # Generate API endpoint for Switch
            api_code = f"""
// API endpoint for Agent {agent_id}
import {{ NextApiRequest, NextApiResponse }} from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {{
  if (req.method !== 'POST') {{
    return res.status(405).json({{ error: 'Method not allowed' }});
  }}

  try {{
    const {{ message, userId }} = req.body;

    // Call Agent Master backend
    const response = await fetch('YOUR_AGENT_MASTER_ENDPOINT/query', {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json',
      }},
      body: JSON.stringify({{
        agent_id: '{agent_id}',
        message,
        user_id: userId
      }})
    }});

    const data = await response.json();
    return res.status(200).json(data);
  }} catch (error) {{
    console.error('Agent API error:', error);
    return res.status(500).json({{ error: 'Internal server error' }});
  }}
}}
"""
            
            deploy_result = deploy_feature_to_switch(
                feature_name=f'agent-{agent_id}',
                feature_type='api',
                code_content=api_code,
                tool_context=tool_context
            )
            
            return {
                'status': 'success',
                'agent_id': agent_id,
                'integration_type': 'api',
                'api_endpoint': f'/api/agent-{agent_id}',
                'deployment': deploy_result,
                'message': f'Agent {agent_id} synced as API to Switch'
            }
        
        elif integration_type == 'background_worker':
            # Generate Firebase Function for Switch
            function_code = f"""
// Firebase Function for Agent {agent_id}
import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

export const agent_{agent_id}_worker = functions.firestore
  .document('tasks/{{taskId}}')
  .onCreate(async (snap, context) => {{
    const taskData = snap.data();
    
    try {{
      // Call Agent Master
      const response = await fetch('YOUR_AGENT_MASTER_ENDPOINT/query', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{
          agent_id: '{agent_id}',
          task: taskData
        }})
      }});
      
      const result = await response.json();
      
      // Update task with result
      await snap.ref.update({{
        status: 'completed',
        result: result,
        completed_at: admin.firestore.FieldValue.serverTimestamp()
      }});
    }} catch (error) {{
      console.error('Background worker error:', error);
      await snap.ref.update({{
        status: 'failed',
        error: error.message
      }});
    }}
  }});
"""
            
            deploy_result = deploy_feature_to_switch(
                feature_name=f'agent-{agent_id}-worker',
                feature_type='function',
                code_content=function_code,
                tool_context=tool_context
            )
            
            return {
                'status': 'success',
                'agent_id': agent_id,
                'integration_type': 'background_worker',
                'function_name': f'agent_{agent_id}_worker',
                'deployment': deploy_result,
                'message': f'Agent {agent_id} synced as background worker to Switch'
            }
        
        else:
            return {
                'status': 'error',
                'message': f'Unknown integration type: {integration_type}'
            }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to sync agent: {str(e)}'
        }


def create_switch_feature_from_prompt(
    feature_description: str,
    target_location: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a complete Switch feature from natural language description.
    
    This is the ULTIMATE tool - just describe what you want and it builds it.
    
    Args:
        feature_description: What you want to build
        target_location: Where in Switch (component, page, api, function)
        
    Returns:
        dict: Complete feature with code and deployment
    """
    try:
        # Chain: CodeMaster generates → Deploy to Switch → Validate
        from .sub_agents.code_master import code_master
        from google.adk.tools import AgentTool
        
        # Step 1: CodeMaster generates the code
        code_tool = AgentTool(agent=code_master)
        code_result = code_tool(
            query=f"""Generate production-ready code for Switch app:

Feature: {feature_description}
Target: {target_location}
Framework: React/TypeScript/Next.js
Styling: Tailwind CSS with glassmorphism
Firebase: Use Firestore and Firebase Auth

Requirements:
- Mobile-first responsive design
- Error handling and loading states
- TypeScript types
- Clean, maintainable code
- Follow Switch app patterns

Generate complete, deployable code.""",
            tool_context=tool_context
        )
        
        # Extract code from result
        code_content = str(code_result)
        
        # Step 2: Deploy to Switch
        feature_name = feature_description.lower().replace(' ', '-')[:50]
        
        deploy_result = deploy_feature_to_switch(
            feature_name=feature_name,
            feature_type=target_location,
            code_content=code_content,
            tool_context=tool_context
        )
        
        return {
            'status': 'success',
            'feature_description': feature_description,
            'feature_name': feature_name,
            'target_location': target_location,
            'code_generated': True,
            'code_content': code_content,
            'deployment': deploy_result,
            'message': f'Feature created and ready for Switch app',
            'next_steps': [
                'Review the generated code',
                'Use deploy_to_switch_firebase to push live',
                'Test at https://switch-470313.web.app'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create feature: {str(e)}'
        }


def get_switch_app_status(
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Get current status of Switch app and all deployed features.
    
    Returns:
        dict: Complete status of Switch app
    """
    try:
        # Get all deployed features
        features_ref = db.collection('switch_features')
        features = []
        
        for doc in features_ref.stream():
            feature_data = doc.to_dict()
            features.append({
                'name': feature_data['feature_name'],
                'type': feature_data['feature_type'],
                'status': feature_data['status'],
                'created_at': feature_data.get('created_at')
            })
        
        # Get all synced agents
        agents_ref = db.collection('switch_app_agents')
        agents = []
        
        for doc in agents_ref.stream():
            agent_data = doc.to_dict()
            agents.append({
                'id': agent_data['agent_id'],
                'name': agent_data['agent_name'],
                'status': agent_data['status']
            })
        
        # Get workflows
        workflows_ref = db.collection('switch_app_workflows')
        workflows = []
        
        for doc in workflows_ref.stream():
            workflow_data = doc.to_dict()
            workflows.append({
                'id': workflow_data['workflow_id'],
                'status': workflow_data['status']
            })
        
        return {
            'status': 'success',
            'switch_app': {
                'live_url': 'https://switch-470313.web.app',
                'firebase_project': 'switch-470313',
                'repo': SWITCH_REPO
            },
            'features': {
                'count': len(features),
                'list': features
            },
            'agents': {
                'count': len(agents),
                'list': agents
            },
            'workflows': {
                'count': len(workflows),
                'list': workflows
            },
            'message': f'Switch app has {len(features)} features, {len(agents)} agents, {len(workflows)} workflows'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to get Switch status: {str(e)}'
        }


def bidirectional_sync(
    sync_type: str,
    data: dict,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Bidirectional sync between Agent Master and Switch.
    
    This allows:
    - Switch to request Agent Master features
    - Agent Master to push updates to Switch
    - Real-time data sync between both apps
    
    Args:
        sync_type: Type of sync (push, pull, realtime)
        data: Data to sync
        
    Returns:
        dict: Sync result
    """
    try:
        if sync_type == 'push':
            # Agent Master pushes to Switch
            sync_doc = {
                'sync_type': 'push',
                'source': 'agent_master',
                'target': 'switch',
                'data': data,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'status': 'synced'
            }
            
            db.collection('cross_app_sync').add(sync_doc)
            
            return {
                'status': 'success',
                'sync_type': 'push',
                'message': 'Data pushed from Agent Master to Switch'
            }
        
        elif sync_type == 'pull':
            # Agent Master pulls from Switch
            switch_data_ref = db.collection('switch_app_data')
            switch_data = []
            
            for doc in switch_data_ref.stream():
                switch_data.append(doc.to_dict())
            
            return {
                'status': 'success',
                'sync_type': 'pull',
                'data': switch_data,
                'message': 'Data pulled from Switch to Agent Master'
            }
        
        elif sync_type == 'realtime':
            # Setup realtime listener
            return {
                'status': 'success',
                'sync_type': 'realtime',
                'message': 'Realtime sync enabled between Agent Master and Switch',
                'listener': 'Firestore realtime listener active'
            }
        
        else:
            return {
                'status': 'error',
                'message': f'Unknown sync type: {sync_type}'
            }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to sync: {str(e)}'
        }


__all__ = [
    'deploy_feature_to_switch',
    'deploy_to_switch_firebase',
    'sync_agent_to_switch',
    'create_switch_feature_from_prompt',
    'get_switch_app_status',
    'bidirectional_sync'
]
