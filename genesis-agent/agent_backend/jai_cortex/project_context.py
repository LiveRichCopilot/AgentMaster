"""
Project Context Manager - Shared memory for all agents
Prevents agents from forgetting what project they're working on
"""

from typing import Dict, Any, Optional
from datetime import datetime
from google.cloud import firestore
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID, database='agent-master-database')


class ProjectContextManager:
    """Manages current project context that all agents can access"""
    
    def __init__(self):
        self.collection = 'agent_project_context'
    
    def set_current_project(
        self,
        session_id: str,
        project_name: str,
        project_path: str,
        description: str = "",
        metadata: Dict[str, Any] = None
    ) -> dict:
        """Set the current project context for a session"""
        try:
            context_doc = {
                'session_id': session_id,
                'project_name': project_name,
                'project_path': project_path,
                'description': description,
                'metadata': metadata or {},
                'last_updated': firestore.SERVER_TIMESTAMP,
                'updated_at_iso': datetime.now().isoformat()
            }
            
            # Use session_id as document ID for easy lookup
            db.collection(self.collection).document(session_id).set(context_doc)
            
            return {
                'status': 'success',
                'message': f'Project context set: {project_name}',
                'project_name': project_name,
                'project_path': project_path
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to set project context: {str(e)}'
            }
    
    def get_current_project(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current project context for a session"""
        try:
            doc = db.collection(self.collection).document(session_id).get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            print(f"Error getting project context: {e}")
            return None
    
    def update_project_metadata(
        self,
        session_id: str,
        metadata_updates: Dict[str, Any]
    ) -> dict:
        """Update project metadata without changing core info"""
        try:
            doc_ref = db.collection(self.collection).document(session_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return {
                    'status': 'error',
                    'message': 'No project context found for this session'
                }
            
            current_data = doc.to_dict()
            current_metadata = current_data.get('metadata', {})
            current_metadata.update(metadata_updates)
            
            doc_ref.update({
                'metadata': current_metadata,
                'last_updated': firestore.SERVER_TIMESTAMP
            })
            
            return {
                'status': 'success',
                'message': 'Project metadata updated',
                'metadata': current_metadata
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to update metadata: {str(e)}'
            }
    
    def clear_project_context(self, session_id: str) -> dict:
        """Clear project context for a session"""
        try:
            db.collection(self.collection).document(session_id).delete()
            return {
                'status': 'success',
                'message': 'Project context cleared'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to clear context: {str(e)}'
            }


# Global instance
project_context_manager = ProjectContextManager()


# Tool functions for agents to use

def remember_project_context(
    project_name: str,
    project_path: str,
    description: str,
    tool_context: ToolContext
) -> dict:
    """Remember the current project context so all agents stay focused.
    
    Use this when starting work on a project so all agents know what you're working on.
    
    Args:
        project_name: Name of the project (e.g., "CortexChat", "Switch V2")
        project_path: Full path to project directory
        description: Brief description of what this project is
        
    Returns:
        dict: Success status
    """
    try:
        # Use session ID from tool context if available
        session_id = getattr(tool_context, 'session_id', 'default_session')
        
        return project_context_manager.set_current_project(
            session_id=session_id,
            project_name=project_name,
            project_path=project_path,
            description=description
        )
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error remembering project: {str(e)}'
        }


def recall_project_context(tool_context: ToolContext) -> dict:
    """Recall what project we're currently working on.
    
    Use this when you're unsure what project you're working on or need to verify context.
    This searches across ALL sessions to find the most recent project context.
    
    Returns:
        dict: Current project information or error if no project set
    """
    try:
        # First try current session
        session_id = getattr(tool_context, 'session_id', 'default_session')
        context = project_context_manager.get_current_project(session_id)
        
        # If not found in current session, find the MOST RECENT project across all sessions
        if not context:
            try:
                recent_contexts = db.collection('agent_project_context')\
                    .order_by('last_updated', direction=firestore.Query.DESCENDING)\
                    .limit(1)\
                    .stream()
                
                for doc in recent_contexts:
                    context = doc.to_dict()
                    # Copy it to current session so we don't lose it
                    project_context_manager.set_current_project(
                        session_id=session_id,
                        project_name=context.get('project_name'),
                        project_path=context.get('project_path'),
                        description=context.get('description', ''),
                        metadata=context.get('metadata', {})
                    )
                    break
            except Exception as e:
                print(f"Error searching for recent context: {e}")
        
        if context:
            return {
                'status': 'success',
                'project_name': context.get('project_name'),
                'project_path': context.get('project_path'),
                'description': context.get('description'),
                'last_updated': context.get('updated_at_iso'),
                'metadata': context.get('metadata', {}),
                'message': f"Currently working on: {context.get('project_name')} (restored from previous session)"
            }
        else:
            return {
                'status': 'no_context',
                'message': 'No project context found in any session. Ask the user what project you should be working on.'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error recalling project: {str(e)}'
        }


def update_project_notes(notes: str, tool_context: ToolContext) -> dict:
    """Add notes to the current project context.
    
    Use this to track important information about the current project.
    
    Args:
        notes: Notes to add to project metadata
        
    Returns:
        dict: Success status
    """
    try:
        session_id = getattr(tool_context, 'session_id', 'default_session')
        
        return project_context_manager.update_project_metadata(
            session_id=session_id,
            metadata_updates={'notes': notes, 'updated_at': datetime.now().isoformat()}
        )
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error updating notes: {str(e)}'
        }
