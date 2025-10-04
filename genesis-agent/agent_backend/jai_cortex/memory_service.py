"""
JAi Cortex OS - Long-Term Memory System (RAG)
Uses Vertex AI Vector Search for infinite memory
"""

import os
from typing import List, Dict, Any
from datetime import datetime
from google.cloud import aiplatform
from google.cloud import firestore

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

# Initialize clients
aiplatform.init(project=PROJECT_ID, location=LOCATION)
db = firestore.Client(project=PROJECT_ID, database='agent-master-database')


class MemoryService:
    """Manages long-term memory using Vertex AI Vector Search"""
    
    def __init__(self):
        self.embedding_model = "text-embedding-004"
        # Vector search endpoint (will be created in Phase 2 setup)
        self.index_endpoint_name = None
        
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text using Vertex AI"""
        try:
            from vertexai.language_models import TextEmbeddingModel
            
            model = TextEmbeddingModel.from_pretrained(self.embedding_model)
            embeddings = model.get_embeddings([text])
            
            return embeddings[0].values  # Returns list of floats
            
        except Exception as e:
            print(f"Embedding generation error: {e}")
            return []
    
    def save_conversation_turn(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        agent_response: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Save a conversation turn to Firestore for later vector indexing"""
        try:
            # Create memory document
            memory_doc = {
                'user_id': user_id,
                'session_id': session_id,
                'user_message': user_message,
                'agent_response': agent_response,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'metadata': metadata or {}
            }
            
            # Save to Firestore
            doc_ref = db.collection('conversation_memory').document()
            doc_ref.set(memory_doc)
            
            # Generate combined text for embedding
            combined_text = f"User: {user_message}\nAgent: {agent_response}"
            
            # Generate embedding (to be indexed later)
            embedding = self.generate_embedding(combined_text)
            
            if embedding:
                # Save the ACTUAL embedding vector for semantic search
                db.collection('memory_embeddings').document(doc_ref.id).set({
                    'conversation_id': doc_ref.id,
                    'embedding': embedding,  # Store the actual vector
                    'embedding_model': self.embedding_model,
                    'text_preview': combined_text[:200],
                    'full_text': combined_text  # Store for retrieval
                })
            
            return doc_ref.id
            
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None
    
    def detect_business_context(self, user_message: str, agent_response: str) -> Dict[str, Any]:
        """
        COGNITIVE MODELING: Detect business context and communication patterns
        
        Analyzes the conversation to identify:
        - Business context (agency, travel, personal, development)
        - Communication style (direct, analytical, creative)
        - Key topics and entities
        """
        combined_text = f"{user_message} {agent_response}".lower()
        
        contexts = {
            'agency': False,
            'travel': False,
            'personal': False,
            'development': False,
            'technical': False
        }
        
        # Context detection patterns
        agency_keywords = ['client', 'campaign', 'marketing', 'brand', 'agency', 'ad', 'creative']
        travel_keywords = ['travel', 'trip', 'destination', 'hotel', 'flight', 'booking', 'tour']
        personal_keywords = ['i feel', 'my life', 'personally', 'my family', 'myself']
        dev_keywords = ['code', 'function', 'api', 'database', 'deploy', 'agent', 'tool', 'github', 'python']
        technical_keywords = ['error', 'bug', 'fix', 'implement', 'architecture', 'system']
        
        # Detect contexts
        if any(keyword in combined_text for keyword in agency_keywords):
            contexts['agency'] = True
        if any(keyword in combined_text for keyword in travel_keywords):
            contexts['travel'] = True
        if any(keyword in combined_text for keyword in personal_keywords):
            contexts['personal'] = True
        if any(keyword in combined_text for keyword in dev_keywords):
            contexts['development'] = True
        if any(keyword in combined_text for keyword in technical_keywords):
            contexts['technical'] = True
        
        # Detect communication style
        style = 'neutral'
        if any(word in user_message.lower() for word in ['analyze', 'explain', 'why', 'how']):
            style = 'analytical'
        elif any(word in user_message.lower() for word in ['create', 'design', 'imagine', 'build']):
            style = 'creative'
        elif len(user_message.split()) < 10:
            style = 'direct'
        
        # Extract key entities (simple version - can be enhanced)
        entities = []
        if 'agent' in combined_text:
            entities.append('agent_development')
        if 'firestore' in combined_text or 'database' in combined_text:
            entities.append('database')
        if 'specialist' in combined_text or 'codemaster' in combined_text:
            entities.append('multi_agent_system')
        
        return {
            'contexts': contexts,
            'primary_context': max(contexts, key=contexts.get) if any(contexts.values()) else 'general',
            'communication_style': style,
            'entities': entities,
            'message_length': len(user_message.split()),
            'timestamp': datetime.now().isoformat()
        }
    
    def auto_capture_conversation(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        agent_response: str
    ) -> str:
        """
        AUTOMATIC COGNITIVE CAPTURE: Saves every conversation with intelligent context detection
        
        This is called automatically after each agent response to build the cognitive model.
        """
        try:
            # Detect business context and communication patterns
            cognitive_analysis = self.detect_business_context(user_message, agent_response)
            
            # Enhanced metadata for cognitive modeling
            metadata = {
                'type': 'auto_captured_conversation',
                'cognitive_analysis': cognitive_analysis,
                'auto_captured': True,
                'capture_timestamp': datetime.now().isoformat()
            }
            
            # Use the existing save method with enhanced metadata
            doc_id = self.save_conversation_turn(
                user_id=user_id,
                session_id=session_id,
                user_message=user_message,
                agent_response=agent_response,
                metadata=metadata
            )
            
            print(f"🧠 Auto-captured conversation with context: {cognitive_analysis['primary_context']}")
            return doc_id
            
        except Exception as e:
            print(f"Error in auto-capture: {e}")
            return None
    
    def search_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search conversation memory using TRUE SEMANTIC SEARCH with vector embeddings
        
        This finds conceptually similar conversations, not just keyword matches.
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            if not query_embedding:
                print("Failed to generate query embedding")
                return []
            
            # Fetch all memory embeddings and compute similarity
            results = []
            embeddings = db.collection('memory_embeddings').stream()
            
            for emb_doc in embeddings:
                emb_data = emb_doc.to_dict()
                stored_embedding = emb_data.get('embedding', [])
                
                if not stored_embedding:
                    continue
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_embedding, stored_embedding)
                
                # Fetch the actual conversation data
                conv_id = emb_data.get('conversation_id')
                conv_doc = db.collection('conversation_memory').document(conv_id).get()
                
                if conv_doc.exists:
                    conv_data = conv_doc.to_dict()
                    results.append({
                        'id': conv_id,
                        'user_message': conv_data.get('user_message', ''),
                        'agent_response': conv_data.get('agent_response', ''),
                        'timestamp': conv_data.get('timestamp'),
                        'relevance': similarity,  # Actual similarity score (0-1)
                        'similarity_score': f"{similarity:.2%}"  # Human readable
                    })
            
            # Sort by similarity (highest first) and return top_k
            results.sort(key=lambda x: x['relevance'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            print(f"Error searching memory: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors (0-1 scale)"""
        try:
            import numpy as np
            
            vec1_np = np.array(vec1)
            vec2_np = np.array(vec2)
            
            dot_product = np.dot(vec1_np, vec2_np)
            norm1 = np.linalg.norm(vec1_np)
            norm2 = np.linalg.norm(vec2_np)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return float(dot_product / (norm1 * norm2))
            
        except Exception as e:
            print(f"Cosine similarity error: {e}")
            return 0.0
    
    def get_conversation_context(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent conversation history for a user"""
        try:
            conversations = db.collection('conversation_memory')\
                .where('user_id', '==', user_id)\
                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            results = []
            for conv in conversations:
                data = conv.to_dict()
                results.append({
                    'user_message': data.get('user_message', ''),
                    'agent_response': data.get('agent_response', ''),
                    'timestamp': data.get('timestamp')
                })
            
            return list(reversed(results))  # Return in chronological order
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def get_cognitive_profile(self, user_id: str = "default_user", days: int = 30) -> Dict[str, Any]:
        """
        COGNITIVE MODELING: Get user's communication patterns and preferences
        
        Analyzes captured conversations to build a profile of:
        - Most common business contexts
        - Communication style patterns
        - Preferred topics
        - Interaction frequency
        """
        try:
            from datetime import timedelta, timezone
            from collections import Counter
            
            # Get recent conversations (use UTC timezone to match Firestore)
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Query ONLY by user_id (no composite index needed)
            # Then filter by timestamp in Python
            conversations = db.collection('conversation_memory')\
                .where('user_id', '==', user_id)\
                .stream()
            
            # Aggregate cognitive data
            contexts_count = Counter()
            styles_count = Counter()
            entities_count = Counter()
            total_messages = 0
            
            for conv in conversations:
                data = conv.to_dict()
                
                # Filter by timestamp in Python (avoid Firestore composite index requirement)
                timestamp = data.get('timestamp')
                if timestamp and timestamp < cutoff_date:
                    continue  # Skip old conversations
                
                total_messages += 1
                user_message = data.get('user_message', '').lower()
                
                metadata = data.get('metadata', {})
                cognitive = metadata.get('cognitive_analysis', {})
                
                # If we have cognitive analysis metadata, use it
                if cognitive:
                    # Count contexts
                    contexts = cognitive.get('contexts', {})
                    for context, is_present in contexts.items():
                        if is_present:
                            contexts_count[context] += 1
                    
                    # Count styles
                    style = cognitive.get('communication_style')
                    if style:
                        styles_count[style] += 1
                    
                    # Count entities
                    entities = cognitive.get('entities', [])
                    for entity in entities:
                        entities_count[entity] += 1
                else:
                    # FALLBACK: Analyze the raw message content
                    # Detect business contexts from keywords
                    if any(word in user_message for word in ['agent', 'cortex', 'code', 'deploy', 'vertex', 'firestore', 'database']):
                        contexts_count['development'] += 1
                    if any(word in user_message for word in ['travel', 'agency', 'booking', 'hotel', 'flight']):
                        contexts_count['travel'] += 1
                    if any(word in user_message for word in ['agency', 'client', 'business', 'marketing']):
                        contexts_count['agency'] += 1
                    if any(word in user_message for word in ['learn', 'autonomous', 'cognitive', 'memory', 'remember']):
                        contexts_count['learning'] += 1
                    
                    # Detect communication style from message patterns
                    if any(word in user_message for word in ['fuck', 'shit', 'damn', 'ass']):
                        styles_count['direct/passionate'] += 1
                    elif '?' in user_message:
                        styles_count['inquisitive'] += 1
                    elif any(word in user_message for word in ['please', 'thanks', 'could you']):
                        styles_count['polite'] += 1
                    else:
                        styles_count['directive'] += 1
                    
                    # Extract key topics (simple word frequency)
                    import re
                    words = re.findall(r'\b[a-z]{4,}\b', user_message)  # Words 4+ chars
                    for word in words:
                        if word not in ['this', 'that', 'with', 'from', 'have', 'want', 'need', 'just', 'like']:
                            entities_count[word] += 1
            
            # Build profile
            profile = {
                'user_id': user_id,
                'analysis_period_days': days,
                'total_conversations': total_messages,
                'primary_contexts': dict(contexts_count.most_common(3)),
                'communication_styles': dict(styles_count.most_common()),
                'key_topics': dict(entities_count.most_common(5)),
                'generated_at': datetime.now().isoformat()
            }
            
            return profile
            
        except Exception as e:
            print(f"Error getting cognitive profile: {e}")
            return {
                'user_id': user_id,
                'analysis_period_days': days,
                'total_conversations': 0,
                'primary_contexts': {},
                'communication_styles': {},
                'key_topics': {},
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }


# Global memory service instance
memory_service = MemoryService()

