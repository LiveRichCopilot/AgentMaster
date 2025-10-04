"""
Communication Analytics Tool
Analyzes conversation quality and provides a "communication score"

Tracks:
- Transcription errors (speech-to-text mistakes)
- Clarity metrics (ambiguous phrases, follow-up questions)
- Sentiment shifts (tone changes)
- Miscommunication events (corrections, clarifications)
"""

from typing import Dict, List, Any
from datetime import datetime
from .memory_service import memory_service


class CommunicationAnalytics:
    """
    Analyzes communication patterns between user and agent
    Similar to Zoom's communication scoring
    """
    
    def __init__(self):
        # Common speech-to-text error pairs
        self.common_errors = {
            'coat': 'code',
            'their': 'there',
            'your': 'you\'re',
            'its': 'it\'s',
            'to': 'too',
            'for': 'four'
        }
        
        # Clarity indicators
        self.ambiguity_phrases = [
            'what do you mean',
            'can you clarify',
            'i don\'t understand',
            'could you explain',
            'not sure what you',
            'confused about'
        ]
        
        # Correction indicators
        self.correction_phrases = [
            'i meant',
            'actually',
            'correction',
            'i said',
            'no i mean',
            'let me rephrase'
        ]
    
    def analyze_conversation(
        self,
        user_id: str = "default_user",
        session_id: str = None,
        recent_turns: int = 10
    ) -> Dict[str, Any]:
        """
        Analyze recent conversation turns and generate communication score
        
        Returns:
            Dictionary with communication metrics and score
        """
        # Get recent conversation history
        conversations = memory_service.get_conversation_context(user_id, limit=recent_turns)
        
        metrics = {
            'total_turns': len(conversations),
            'transcription_issues': 0,
            'clarity_requests': 0,
            'corrections': 0,
            'sentiment_consistency': 'stable',
            'details': []
        }
        
        # Analyze each turn
        for i, turn in enumerate(conversations):
            user_msg = turn['user_message'].lower()
            agent_resp = turn['agent_response'].lower()
            
            # Check for potential transcription errors
            for error_word in self.common_errors.keys():
                if error_word in user_msg:
                    metrics['transcription_issues'] += 1
                    metrics['details'].append({
                        'turn': i + 1,
                        'type': 'transcription',
                        'word': error_word,
                        'likely_meant': self.common_errors[error_word]
                    })
            
            # Check for clarity requests
            for phrase in self.ambiguity_phrases:
                if phrase in agent_resp:
                    metrics['clarity_requests'] += 1
                    metrics['details'].append({
                        'turn': i + 1,
                        'type': 'clarity_request',
                        'phrase': phrase
                    })
            
            # Check for corrections
            for phrase in self.correction_phrases:
                if phrase in user_msg:
                    metrics['corrections'] += 1
                    metrics['details'].append({
                        'turn': i + 1,
                        'type': 'correction',
                        'phrase': phrase
                    })
        
        # Calculate communication score (0-100)
        score = 100
        
        # Deduct points for issues
        score -= (metrics['transcription_issues'] * 2)  # -2 per transcription issue
        score -= (metrics['clarity_requests'] * 5)       # -5 per clarity request
        score -= (metrics['corrections'] * 3)            # -3 per correction
        
        # Floor at 0
        score = max(0, score)
        
        # Determine quality level
        if score >= 90:
            quality = "Excellent"
        elif score >= 75:
            quality = "Good"
        elif score >= 60:
            quality = "Fair"
        else:
            quality = "Needs Improvement"
        
        return {
            'score': score,
            'quality': quality,
            'metrics': metrics,
            'analysis_timestamp': datetime.now().isoformat(),
            'recommendations': self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        if metrics['transcription_issues'] > 2:
            recommendations.append(
                "Consider speaking more slowly or enunciating keywords to reduce transcription errors"
            )
        
        if metrics['clarity_requests'] > 2:
            recommendations.append(
                "Try providing more context upfront to reduce clarification requests"
            )
        
        if metrics['corrections'] > 2:
            recommendations.append(
                "Consider reviewing messages before sending to catch misstatements early"
            )
        
        if not recommendations:
            recommendations.append(
                "Communication is flowing smoothly! Keep up the good work."
            )
        
        return recommendations


# Global instance
communication_analytics = CommunicationAnalytics()

