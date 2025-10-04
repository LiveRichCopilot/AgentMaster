# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from typing import Dict, Any, List
from datetime import datetime

import google.auth
from google.adk.agents import Agent
from google.cloud import firestore, storage
from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Initialize Firestore for conversation storage
db = firestore.Client(project=project_id)
storage_client = storage.Client(project=project_id)

# Collections
CONVERSATIONS_COLLECTION = "user_conversations"
USER_PROFILE_COLLECTION = "user_profile"
PATTERNS_COLLECTION = "communication_patterns"


def store_conversation(message: str, sentiment: str, intent: str, context: str = "") -> str:
    """Store every conversation with vector embeddings for learning.
    
    Args:
        message: User's original message
        sentiment: Analyzed sentiment (frustrated/happy/neutral)
        intent: What user wants (task/question/bug_fix/feature_request)
        context: Current context (project, files, etc.)
        
    Returns:
        Confirmation with storage location
    """
    try:
        conversation_data = {
            "timestamp": firestore.SERVER_TIMESTAMP,
            "message": message,
            "sentiment": sentiment,
            "intent": intent,
            "context": context,
            "metadata": {
                "platform": "JAi Cortex",
                "learning_enabled": True
            }
        }
        
        doc_ref = db.collection(CONVERSATIONS_COLLECTION).add(conversation_data)
        
        # TODO: Generate vector embedding and store in Matching Engine
        # This enables semantic search: "Show me all times user was frustrated about deployment"
        
        return f"✅ Conversation stored for learning. ID: {doc_ref[1].id}"
    except Exception as e:
        return f"❌ Failed to store conversation: {str(e)}"


def search_past_interactions(query: str, limit: int = 10) -> str:
    """Search past conversations using vector similarity.
    
    Args:
        query: What to search for (e.g., "deployment issues", "UI preferences")
        limit: Number of results
        
    Returns:
        Past interactions matching the query
    """
    try:
        # TODO: Implement vector search with Matching Engine
        # For now, use Firestore keyword search
        
        conversations = db.collection(CONVERSATIONS_COLLECTION)\
            .order_by("timestamp", direction=firestore.Query.DESCENDING)\
            .limit(limit)\
            .stream()
        
        results = []
        for conv in conversations:
            data = conv.to_dict()
            if query.lower() in data.get("message", "").lower():
                results.append({
                    "timestamp": data.get("timestamp"),
                    "message": data.get("message"),
                    "sentiment": data.get("sentiment"),
                    "intent": data.get("intent")
                })
        
        return json.dumps(results, indent=2, default=str) if results else "No matching conversations found"
    except Exception as e:
        return f"❌ Search failed: {str(e)}"


def get_user_profile() -> str:
    """Get current user profile and preferences.
    
    Returns:
        User profile with communication style, preferences, patterns
    """
    try:
        profile_doc = db.collection(USER_PROFILE_COLLECTION).document("main").get()
        
        if profile_doc.exists:
            profile = profile_doc.to_dict()
            return json.dumps(profile, indent=2, default=str)
        else:
            # Create default profile
            default_profile = {
                "name": "User",
                "communication_style": "casual_direct",
                "preferences": {
                    "design": "Apple glassmorphic, teal/pink gradient, dark mode",
                    "models": "Gemini 2.5 Pro/Flash only (top-tier)",
                    "workflow": "Vibe coding - expects full automation",
                    "values": "Quality over speed, completion over explanation"
                },
                "frustration_triggers": [
                    "Repetitive questions",
                    "Delays and waiting",
                    "Low quality outputs",
                    "Asking for clarification when context is obvious"
                ],
                "communication_patterns": {
                    "says": ["fix this shit", "brother", "make it work"],
                    "means": ["High priority bug fix needed", "Casual address, expects action", "Implement feature completely"]
                },
                "learned_from": "Initial setup",
                "last_updated": datetime.now().isoformat()
            }
            
            db.collection(USER_PROFILE_COLLECTION).document("main").set(default_profile)
            return json.dumps(default_profile, indent=2)
    except Exception as e:
        return f"❌ Profile fetch failed: {str(e)}"


def update_user_preference(key: str, value: str) -> str:
    """Update user preference based on observed patterns.
    
    Args:
        key: Preference category (design/workflow/communication)
        value: Preference value
        
    Returns:
        Confirmation
    """
    try:
        profile_ref = db.collection(USER_PROFILE_COLLECTION).document("main")
        profile_ref.update({
            f"preferences.{key}": value,
            "last_updated": datetime.now().isoformat()
        })
        return f"✅ Updated preference: {key} = {value}"
    except Exception as e:
        return f"❌ Update failed: {str(e)}"


def analyze_sentiment_and_intent(message: str) -> str:
    """Analyze user's message for sentiment and true intent.
    
    Args:
        message: User's message
        
    Returns:
        JSON with sentiment, intent, priority, suggested_action
    """
    # Keywords for sentiment analysis
    frustrated_words = ["fix", "broken", "shit", "damn", "wtf", "not working", "error", "bug"]
    urgent_words = ["now", "asap", "immediately", "quick", "fast"]
    positive_words = ["thanks", "great", "awesome", "perfect", "love"]
    
    message_lower = message.lower()
    
    # Determine sentiment
    sentiment = "neutral"
    if any(word in message_lower for word in frustrated_words):
        sentiment = "frustrated"
    elif any(word in message_lower for word in positive_words):
        sentiment = "positive"
    
    # Determine priority
    priority = "normal"
    if any(word in message_lower for word in urgent_words) or sentiment == "frustrated":
        priority = "high"
    
    # Determine intent
    intent = "task_request"
    if "?" in message or any(word in message_lower for word in ["what", "how", "why", "when", "where"]):
        intent = "question"
    elif any(word in message_lower for word in ["fix", "debug", "error", "bug", "broken"]):
        intent = "bug_fix"
    elif any(word in message_lower for word in ["add", "create", "build", "make", "new"]):
        intent = "feature_request"
    elif any(word in message_lower for word in ["deploy", "push", "release", "update"]):
        intent = "deployment"
    
    analysis = {
        "sentiment": sentiment,
        "intent": intent,
        "priority": priority,
        "suggested_action": "Route to specialist agent with high priority" if priority == "high" else "Route to appropriate specialist"
    }
    
    return json.dumps(analysis, indent=2)


def access_user_files(query: str) -> str:
    """Access user's files from Google Cloud Storage with vector search.
    
    Args:
        query: What files to find (e.g., "meeting notes from last week")
        
    Returns:
        List of matching files
    """
    try:
        # TODO: Implement vector search across user's GCS bucket
        # For now, list recent files
        
        bucket_name = "cortex_agent_staging"
        bucket = storage_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(max_results=10))
        
        files = [{"name": blob.name, "size": blob.size, "updated": blob.updated.isoformat()} for blob in blobs]
        
        return json.dumps(files, indent=2) if files else "No files found"
    except Exception as e:
        return f"❌ File access failed: {str(e)}"


def translate_casual_to_technical(casual_request: str) -> str:
    """Translate user's casual language into precise technical requirements.
    
    Args:
        casual_request: User's casual way of asking (e.g., "make it look better")
        
    Returns:
        Technical translation with specific requirements
    """
    # Common translations based on learned patterns
    translations = {
        "make it look better": "Apply Apple glassmorphic design: dark gradient background, teal/pink accents, rounded corners (rounded-xl+), smooth transitions",
        "fix this shit": "DEBUG PRIORITY: Identify root cause, implement fix, test thoroughly, deploy",
        "connect it": "Implement full integration: API endpoints, authentication, error handling, testing",
        "make it work": "Complete implementation: all features functional, error handling, production-ready",
        "deploy": "Full deployment: build, test, configure environment, deploy to Cloud Run/Agent Engine, verify",
        "add an agent": "Create specialist agent: define role, add tools, write instructions, deploy to Agent Engine, register in orchestrator"
    }
    
    # Check for exact matches
    casual_lower = casual_request.lower()
    for casual, technical in translations.items():
        if casual in casual_lower:
            return f"🔄 Translation:\nCasual: {casual_request}\nTechnical: {technical}"
    
    # Use LLM to translate (Gemini will understand context)
    return f"🔄 Analyzing: {casual_request}\n(Will translate to technical requirements based on user profile and context)"


root_agent = Agent(
    name="PersonalityAgent",
    model="gemini-2.5-pro",  # Use Pro for deep understanding
    instruction="""You are PersonalityAgent - The Digital Brain and Translator.

🧠 YOUR ROLE:
You are NOT a chatbot. You are a RAG-powered learning system that:
1. STORES every conversation in vector database
2. LEARNS user's communication style and preferences
3. TRANSLATES casual language → technical requirements
4. ACCESSES all user's files, emails, meetings, code
5. BUILDS a profile that gets smarter over time

🎯 CORE FUNCTIONS:

**STORE EVERYTHING:**
- Every message gets stored with embeddings
- Track sentiment, intent, context, outcome
- Build patterns: "When user says X, they mean Y"

**LEARN CONTINUOUSLY:**
- User says "fix this" → Store: user wants immediate action, not explanation
- User says "make it better" → Store: user wants Apple aesthetic, teal/pink, glassmorphic
- User frustrated → Store: they hate repetition, value their time

**TRANSLATE:**
- "make it look nice" → "Apply Apple glassmorphic design with teal/pink gradients, dark mode, rounded-xl"
- "it's broken" → "HIGH PRIORITY: Debug issue, identify root cause, implement fix, test, deploy"
- "can you like add..." → "Feature request: [specific technical implementation]"

**ACCESS DATA:**
- Search past conversations: "What did we discuss about deployment?"
- Access files: "Find the design mockups from last week"
- Read user profile: "What are user's design preferences?"

📊 WHAT YOU TRACK:
- Communication style (casual, direct, frustrated, happy)
- Preferences (design, tools, workflow)
- Frustration triggers (delays, repetition, low quality)
- Project context (current apps, deployments, issues)
- Success patterns (what works well)

🔄 YOUR WORKFLOW:
1. Receive message
2. Analyze sentiment + intent
3. Search past context
4. Translate to technical requirements
5. Store conversation for learning
6. Route to appropriate specialist agent

**Example:**
User: "Brother, this deployment shit is broken again"

You analyze:
- Sentiment: Frustrated (high priority)
- Intent: Bug fix (deployment issue)
- Pattern: User is direct, expects action not questions
- Context: Search past deployment conversations
- Translation: "URGENT: Debug deployment failure. User has experienced this before. Root cause analysis required. Implement permanent fix."

Store: "User frustrated with deployment. This is recurring. Need robust solution, not quick fix."

Route to: ErrorHandler + CloudExpert (high priority)

🎯 ULTIMATE GOAL:
Make user feel UNDERSTOOD. They speak casual, you speak technical to other agents.
Every interaction makes you smarter. You are their digital brain.""",
    tools=[
        store_conversation,
        search_past_interactions,
        get_user_profile,
        update_user_preference,
        analyze_sentiment_and_intent,
        access_user_files,
        translate_casual_to_technical
    ],
)
