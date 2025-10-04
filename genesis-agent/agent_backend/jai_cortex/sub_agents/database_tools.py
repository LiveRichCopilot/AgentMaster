"""
Database Tools for DatabaseExpert
Modular Firestore query and analysis functions
"""

import os
from typing import Optional, Dict, List, Any
from google.adk.tools import ToolContext
from google.cloud import firestore
from google.api_core import exceptions as gcp_exceptions
import google.auth

# Get project ID and database ID
try:
    credentials, project_id = google.auth.default()
    PROJECT_ID = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT', 'studio-2416451423-f2d96')
except Exception:
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'studio-2416451423-f2d96')

DATABASE_ID = 'agent-master-database'


def query_firestore_collection(
    collection_name: str,
    limit: int = 10,
    database_id: str = 'agent-master-database',
    tool_context: ToolContext = None
) -> dict:
    """Query a Firestore collection and return documents."""
    try:
        db = firestore.Client(project=PROJECT_ID, database=database_id)
        collection_ref = db.collection(collection_name)
        docs = list(collection_ref.limit(limit).stream())
        
        if not docs:
            return {
                'status': 'success',
                'collection': collection_name,
                'total_retrieved': 0,
                'documents': [],
                'message': f'Collection "{collection_name}" exists but is empty'
            }
        
        documents = []
        field_types = {}
        
        for doc in docs:
            doc_data = doc.to_dict()
            documents.append({'id': doc.id, 'data': doc_data})
            
            for field, value in doc_data.items():
                field_type = type(value).__name__
                if field not in field_types:
                    field_types[field] = set()
                field_types[field].add(field_type)
        
        field_types_list = {field: list(types) for field, types in field_types.items()}
        
        return {
            'status': 'success',
            'collection': collection_name,
            'database_id': database_id,
            'total_retrieved': len(documents),
            'documents': documents,
            'schema': field_types_list,
            'message': f'Retrieved {len(documents)} documents from {collection_name}'
        }
    except gcp_exceptions.PermissionDenied:
        return {'status': 'error', 'message': 'Permission denied. Need roles/datastore.user role'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error querying Firestore: {str(e)}'}


def analyze_collection_schema(
    collection_name: str,
    sample_size: int = 100,
    database_id: str = 'agent-master-database',
    tool_context: ToolContext = None
) -> dict:
    """Analyze the schema and structure of a Firestore collection."""
    try:
        db = firestore.Client(project=PROJECT_ID, database=database_id)
        collection_ref = db.collection(collection_name)
        docs = list(collection_ref.limit(sample_size).stream())
        
        if not docs:
            return {'status': 'success', 'collection': collection_name, 'message': 'Collection is empty'}
        
        field_analysis = {}
        total_docs = len(docs)
        
        for doc in docs:
            doc_data = doc.to_dict()
            for field, value in doc_data.items():
                if field not in field_analysis:
                    field_analysis[field] = {
                        'types': set(), 'count': 0, 'is_array': False, 
                        'is_nested': False, 'sample_values': []
                    }
                
                field_analysis[field]['count'] += 1
                field_analysis[field]['types'].add(type(value).__name__)
                
                if isinstance(value, list):
                    field_analysis[field]['is_array'] = True
                if isinstance(value, dict):
                    field_analysis[field]['is_nested'] = True
                
                if len(field_analysis[field]['sample_values']) < 3:
                    if not isinstance(value, (dict, list)):
                        field_analysis[field]['sample_values'].append(value)
        
        schema_report = {}
        for field, analysis in field_analysis.items():
            schema_report[field] = {
                'types': list(analysis['types']),
                'frequency': f"{(analysis['count'] / total_docs * 100):.1f}%",
                'appears_in': f"{analysis['count']}/{total_docs} documents",
                'is_array': analysis['is_array'],
                'is_nested': analysis['is_nested'],
                'sample_values': analysis['sample_values']
            }
        
        return {
            'status': 'success',
            'collection': collection_name,
            'database_id': database_id,
            'documents_analyzed': total_docs,
            'total_fields': len(schema_report),
            'schema': schema_report,
            'message': f'Analyzed {total_docs} documents from {collection_name}'
        }
    except Exception as e:
        return {'status': 'error', 'message': f'Error analyzing schema: {str(e)}'}


def get_collection_stats(
    collection_name: str,
    database_id: str = 'agent-master-database',
    tool_context: ToolContext = None
) -> dict:
    """Get detailed statistics for a Firestore collection."""
    try:
        db = firestore.Client(project=PROJECT_ID, database=database_id)
        collection_ref = db.collection(collection_name)
        sample_docs = list(collection_ref.limit(200).stream())
        
        if not sample_docs:
            return {'status': 'success', 'collection': collection_name, 'document_count': 0, 'message': 'Empty'}
        
        total_size = 0
        field_counts = {}
        
        for doc in sample_docs:
            doc_data = doc.to_dict()
            total_size += len(str(doc_data))
            for field in doc_data.keys():
                field_counts[field] = field_counts.get(field, 0) + 1
        
        avg_size = total_size / len(sample_docs)
        most_common = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'status': 'success',
            'collection': collection_name,
            'database_id': database_id,
            'statistics': {
                'sample_size': len(sample_docs),
                'estimated_avg_doc_size_bytes': int(avg_size),
                'total_unique_fields': len(field_counts),
                'most_common_fields': [
                    {'field': f, 'appears_in': c, 'frequency': f"{(c/len(sample_docs)*100):.1f}%"}
                    for f, c in most_common
                ]
            },
            'message': f'Statistics based on {len(sample_docs)} sample documents'
        }
    except Exception as e:
        return {'status': 'error', 'message': f'Error getting stats: {str(e)}'}


def check_firestore_indexes(
    database_id: str = 'agent-master-database',
    tool_context: ToolContext = None
) -> dict:
    """Get Firestore index recommendations and best practices."""
    recommendations = {
        'general_tips': [
            'Firestore automatically indexes every field in a document',
            'Composite indexes needed for queries with multiple filters or orderBy',
            'Create indexes through Firebase console or firebase.indexes.json'
        ],
        'common_patterns': {
            'equality_filter': 'Single-field indexes (automatic)',
            'range_filter': 'Single-field indexes (automatic)',
            'multiple_filters': 'Composite index required',
            'order_by_with_filter': 'Composite index required'
        },
        'optimization_tips': [
            'Use .where() filters before .orderBy() for better performance',
            'Avoid queries with multiple array-contains filters',
            'Use subcollections for hierarchical data',
            'Monitor query performance in Cloud Console'
        ]
    }
    
    return {
        'status': 'success',
        'database_id': database_id,
        'recommendations': recommendations,
        'message': 'Index recommendations and best practices'
    }


def optimize_firestore_query(query_description: str, tool_context: ToolContext) -> dict:
    """Analyze a Firestore query and suggest optimizations."""
    optimizations = {
        'analysis': f'Analyzing query: {query_description}',
        'recommendations': [],
        'best_practices': [
            'Use pagination (limit + startAfter) for large result sets',
            'Cache frequently accessed data',
            'Use batch operations for multiple writes',
            'Use subcollections for 1-to-many relationships'
        ]
    }
    
    query_lower = query_description.lower()
    
    if 'where' in query_lower and 'order' in query_lower:
        optimizations['recommendations'].append({
            'issue': 'Multiple filters with orderBy detected',
            'solution': 'Create a composite index for this query',
            'impact': 'Required - query will fail without this index'
        })
    
    if 'all' in query_lower or 'every' in query_lower:
        optimizations['recommendations'].append({
            'issue': 'Retrieving all documents',
            'solution': 'Use pagination with limit() and startAfter()',
            'impact': 'Reduces read costs and improves performance'
        })
    
    if not optimizations['recommendations']:
        optimizations['recommendations'].append({
            'message': 'No obvious performance issues detected',
            'tip': 'Use appropriate indexes and pagination for production'
        })
    
    return {
        'status': 'success',
        'query': query_description,
        'optimizations': optimizations,
        'message': 'Query analysis complete'
    }


def get_database_recommendations(tool_context: ToolContext) -> dict:
    """Get Firestore best practices and recommendations."""
    recommendations = {
        'data_modeling': [
            'Use flat data structures (avoid deep nesting)',
            'Denormalize data for read-heavy workloads',
            'Use subcollections for one-to-many relationships',
            'Keep document sizes under 1MB'
        ],
        'performance': [
            'Create indexes for all queries with filters',
            'Use batched writes for multiple operations',
            'Implement pagination for large result sets',
            'Cache frequently accessed data'
        ],
        'cost_optimization': [
            'Use limit() to avoid unnecessary reads',
            'Delete old data to reduce storage costs',
            'Monitor usage in Cloud Console',
            'Use Firebase Local Emulator for testing'
        ],
        'security': [
            'Always use Firestore Security Rules',
            'Validate data on both client and server',
            'Use server-side timestamps',
            'Implement proper authentication'
        ]
    }
    
    return {
        'status': 'success',
        'recommendations': recommendations,
        'message': 'Firestore best practices'
    }


def get_cognitive_profile(user_id: str = "default_user", days: int = 30, tool_context: ToolContext = None) -> Dict[str, Any]:
    """Get the user's cognitive profile - communication patterns and business contexts.
    
    Analyzes captured conversations to understand:
    - Primary business contexts (agency, travel, personal, development)
    - Communication style preferences
    - Key topics of interest
    - Interaction patterns
    
    Args:
        user_id: User identifier (default: "default_user")
        days: Number of days to analyze (default: 30)
        
    Returns:
        Dictionary with cognitive profile analysis
    """
    try:
        from ..memory_service import memory_service
        
        profile = memory_service.get_cognitive_profile(user_id=user_id, days=days)
        
        return {
            'status': 'success',
            'profile': profile,
            'message': f"Analyzed {profile['total_conversations']} conversations from the last {days} days"
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error getting cognitive profile: {str(e)}'
        }


def find_notes(tool_context: ToolContext = None) -> Dict[str, Any]:
    """Find all saved notes in the conversation_memory collection.
    
    Notes are stored in conversation_memory with metadata.type='note'.
    This function retrieves all notes and displays them with their titles and content.
    
    Returns:
        Dictionary with status and list of all found notes
    """
    try:
        db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
        
        # Query conversation_memory for documents where metadata.type = 'note'
        notes_query = db.collection('conversation_memory').where('metadata.type', '==', 'note')
        
        notes_list = []
        for doc in notes_query.stream():
            data = doc.to_dict()
            notes_list.append({
                'id': doc.id,
                'title': data.get('metadata', {}).get('title', 'Untitled'),
                'content': data.get('agent_response', ''),
                'timestamp': data.get('timestamp', 'Unknown'),
                'user_message': data.get('user_message', '')
            })
        
        if not notes_list:
            return {
                'status': 'success',
                'message': 'No notes found in the database',
                'notes': []
            }
        
        # Sort by timestamp (most recent first)
        notes_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            'status': 'success',
            'message': f'Found {len(notes_list)} note(s)',
            'notes': notes_list,
            'summary': f"You have {len(notes_list)} saved notes. The most recent is '{notes_list[0]['title']}'"
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error finding notes: {str(e)}'
        }

