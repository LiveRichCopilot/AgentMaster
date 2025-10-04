"""
Cognitive Modeling Middleware
Automatically captures every conversation for cognitive profiling
"""

import os
from typing import Dict, Any
from .memory_service import memory_service


class CognitiveMiddleware:
    """
    Middleware that automatically captures conversations with context detection
    
    This is the bridge between the ADK agent and the cognitive modeling system.
    """
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.capture_count = 0
        
    def capture_conversation(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        agent_response: str
    ) -> Dict[str, Any]:
        """
        Automatically capture and analyze a conversation turn
        
        Returns the cognitive analysis for logging/debugging
        """
        if not self.enabled:
            return {'status': 'disabled'}
        
        try:
            # Call the memory service auto-capture
            doc_id = memory_service.auto_capture_conversation(
                user_id=user_id,
                session_id=session_id,
                user_message=user_message,
                agent_response=agent_response
            )
            
            self.capture_count += 1
            
            return {
                'status': 'success',
                'doc_id': doc_id,
                'capture_count': self.capture_count
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get middleware statistics"""
        return {
            'enabled': self.enabled,
            'total_captured': self.capture_count
        }


# Global middleware instance
cognitive_middleware = CognitiveMiddleware(
    enabled=os.environ.get('COGNITIVE_CAPTURE', 'true').lower() == 'true'
)

