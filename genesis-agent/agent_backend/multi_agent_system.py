"""
MULTI-AGENT SYSTEM
Manages multiple specialist agents, routes messages, handles multi-platform
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from agent_templates import AGENT_TEMPLATES, calculate_agent_strength

# ============================================================================
# AGENT MANAGER
# ============================================================================

class AgentManager:
    """Manages multiple specialist agents"""
    
    def __init__(self):
        self.agents = {}
        self.agent_metrics = {}
        self.conversations = {}
        
    def create_agent(self, template_name: str, custom_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new agent from template"""
        if template_name not in AGENT_TEMPLATES:
            return {'status': 'error', 'message': f'Template {template_name} not found'}
        
        template = AGENT_TEMPLATES[template_name]
        agent_id = custom_name or template['name']
        
        self.agents[agent_id] = {
            'id': agent_id,
            'template': template_name,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            **template
        }
        
        # Initialize metrics
        self.agent_metrics[agent_id] = {
            'tasks_completed': 0,
            'success_rate': 100.0,
            'response_time': 2.0,
            'user_satisfaction': 5.0,
            'proactive_alerts': 0,
            'last_active': datetime.now().isoformat()
        }
        
        return {
            'status': 'success',
            'message': f'Agent {agent_id} created',
            'agent': self.agents[agent_id]
        }
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents with their strength"""
        agents_with_strength = []
        
        for agent_id, agent in self.agents.items():
            metrics = self.agent_metrics.get(agent_id, {})
            strength = calculate_agent_strength(agent_id, metrics)
            
            agents_with_strength.append({
                'id': agent_id,
                'name': agent['name'],
                'role': agent['role'],
                'status': agent['status'],
                'strength': strength
            })
        
        return agents_with_strength
    
    def get_agent_strength(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed strength metrics for an agent"""
        if agent_id not in self.agent_metrics:
            return {'status': 'error', 'message': 'Agent not found'}
        
        metrics = self.agent_metrics[agent_id]
        strength = calculate_agent_strength(agent_id, metrics)
        
        return {
            'status': 'success',
            'agent_id': agent_id,
            **strength
        }
    
    def update_metrics(self, agent_id: str, update: Dict[str, Any]):
        """Update agent metrics after task"""
        if agent_id not in self.agent_metrics:
            return
        
        metrics = self.agent_metrics[agent_id]
        
        if 'task_completed' in update:
            metrics['tasks_completed'] += 1
        
        if 'success' in update:
            # Running average
            current_rate = metrics['success_rate']
            total_tasks = metrics['tasks_completed']
            new_success = 100 if update['success'] else 0
            metrics['success_rate'] = ((current_rate * (total_tasks - 1)) + new_success) / total_tasks
        
        if 'response_time' in update:
            # Running average
            current_time = metrics['response_time']
            total_tasks = metrics['tasks_completed']
            metrics['response_time'] = ((current_time * (total_tasks - 1)) + update['response_time']) / total_tasks
        
        if 'proactive_alert' in update:
            metrics['proactive_alerts'] += 1
        
        metrics['last_active'] = datetime.now().isoformat()
    
    def route_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Route message to best agent based on content"""
        message_lower = message.lower()
        
        # Crypto keywords (check first - most specific)
        if any(word in message_lower for word in ['crypto', 'bitcoin', 'ethereum', 'btc', 'eth', 'defi', 'nft', 'blockchain', 'altcoin', 'wallet']):
            return 'CryptoKing'
        
        # Stock keywords
        if any(word in message_lower for word in ['stock', 'stocks', 'shares', 'dividend', 'portfolio', 'market', 'nasdaq', 'dow', 'earnings']):
            return 'StockMaster'
        
        # Financial keywords (general)
        if any(word in message_lower for word in ['money', 'budget', 'expense', 'finance', 'transaction', 'cost', 'price', 'invest', 'saving']):
            return 'FinanceWizard'
        
        # Code keywords
        if any(word in message_lower for word in [
            'code', 'coding', 'bug', 'debug', 'deploy', 'test', 'testing', 'function', 
            'react', 'python', 'javascript', 'typescript', 'api', 'backend', 'frontend',
            'database', 'firestore', 'sql', 'query', 'schema', 'collection', 'document',
            'app', 'application', 'build', 'compile', 'error', 'exception', 'fix',
            'refactor', 'optimize', 'performance', 'script', 'library', 'framework',
            'node', 'npm', 'package', 'dependency', 'git', 'repository', 'commit'
        ]):
            return 'CodeMaster'
        
        # Research keywords
        if any(word in message_lower for word in ['search', 'find', 'research', 'competitor', 'trend', 'news', 'article']):
            return 'ResearchScout'
        
        # Design keywords
        if any(word in message_lower for word in ['design', 'ui', 'ux', 'color', 'layout', 'component', 'style', 'glassmorphic']):
            return 'DesignGenius'
        
        # Travel keywords
        if any(word in message_lower for word in ['travel', 'flight', 'hotel', 'trip', 'vacation', 'destination', 'booking']):
            return 'TravelGenius'
        
        # Shopping keywords
        if any(word in message_lower for word in ['shop', 'shopping', 'buy', 'purchase', 'deal', 'price compare', 'product']):
            return 'ShopSavvy'
        
        # Budget keywords
        if any(word in message_lower for word in ['spending', 'bill', 'subscription', 'save money', 'track expense']):
            return 'BudgetBoss'
        
        # Sports keywords
        if any(word in message_lower for word in ['sports', 'game', 'team', 'prediction', 'bet', 'odds', 'nfl', 'nba', 'soccer']):
            return 'SportsMath'
        
        # Automation keywords
        if any(word in message_lower for word in ['automate', 'automation', 'workflow', 'schedule', 'trigger', 'cron']):
            return 'AutomationWizard'
        
        # Notebook/Data science keywords
        if any(word in message_lower for word in ['notebook', 'jupyter', 'data analysis', 'dataset', 'pandas', 'visualization']):
            return 'NotebookGenius'
        
        # Maps keywords
        if any(word in message_lower for word in ['map', 'maps', 'location', 'directions', 'navigate', 'route', 'gps']):
            return 'MapsNavigator'
        
        # Workspace keywords
        if any(word in message_lower for word in ['email', 'gmail', 'drive', 'calendar', 'meeting', 'doc', 'sheet']):
            return 'WorkspaceManager'
        
        # Media keywords
        if any(word in message_lower for word in ['zoom', 'video', 'audio', 'transcribe', 'recording']):
            return 'MediaProcessor'
        
        # Agent creation keywords
        if any(word in message_lower for word in ['create agent', 'new agent', 'build agent', 'make agent']):
            return 'AgentCreator'
        
        # Default to master agent
        return 'CORTEX_MASTER'


# ============================================================================
# MULTI-PLATFORM ROUTER
# ============================================================================

class MultiPlatformRouter:
    """Routes messages from different platforms (Web, Telegram, WhatsApp)"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.platform_sessions = {}
    
    def handle_message(self, message: str, platform: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """Handle message from any platform"""
        
        # Determine which agent should handle this
        agent_id = self.agent_manager.route_message(message)
        agent = self.agent_manager.get_agent(agent_id)
        
        if not agent:
            # Fallback to master
            agent_id = 'CORTEX_MASTER'
        
        # Log the interaction
        session_key = f"{platform}:{user_id}:{session_id}"
        if session_key not in self.platform_sessions:
            self.platform_sessions[session_key] = {
                'platform': platform,
                'user_id': user_id,
                'session_id': session_id,
                'messages': [],
                'agent_id': agent_id,
                'started_at': datetime.now().isoformat()
            }
        
        self.platform_sessions[session_key]['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'role': 'user',
            'content': message,
            'agent_assigned': agent_id
        })
        
        return {
            'status': 'success',
            'agent_id': agent_id,
            'agent_name': agent.get('name', 'Cortex') if agent else 'Cortex',
            'platform': platform,
            'session_key': session_key
        }
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get statistics across all platforms"""
        platform_counts = {}
        
        for session in self.platform_sessions.values():
            platform = session['platform']
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return {
            'total_sessions': len(self.platform_sessions),
            'platforms': platform_counts,
            'active_agents': len(self.agent_manager.agents)
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton instances
_agent_manager = None
_router = None

def get_agent_manager() -> AgentManager:
    """Get or create agent manager"""
    global _agent_manager
    if _agent_manager is None:
        _agent_manager = AgentManager()
        # Create default agents
        for template_name in AGENT_TEMPLATES.keys():
            _agent_manager.create_agent(template_name)
    return _agent_manager

def get_router() -> MultiPlatformRouter:
    """Get or create router"""
    global _router
    if _router is None:
        _router = MultiPlatformRouter(get_agent_manager())
    return _router
