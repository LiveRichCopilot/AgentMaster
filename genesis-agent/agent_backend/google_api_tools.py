"""
Real Google Cloud API tools for specialist agents
Uses the APIs the user has enabled
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64

# Google Cloud APIs
from google.cloud import storage, language_v1, vision, speech_v1, translate_v2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

PROJECT_ID = "studio-2416451423-f2d96"

# Initialize clients
storage_client = storage.Client(project=PROJECT_ID)
language_client = language_v1.LanguageServiceClient()
vision_client = vision.ImageAnnotatorClient()
speech_client = speech_v1.SpeechClient()
translate_client = translate_v2.Client()

# Workspace APIs (Gmail, Drive, Calendar, Sheets)
def get_workspace_service(api_name: str, version: str):
    """Get authenticated Google Workspace service"""
    # Uses application default credentials
    return build(api_name, version)


# ============================================================================
# PERSONALITYAGENT - Real Sentiment Analysis
# ============================================================================

def analyze_sentiment_with_ai(text: str) -> Dict[str, Any]:
    """Use Cloud Natural Language API for REAL sentiment analysis"""
    try:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        # Analyze sentiment
        sentiment = language_client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        
        # Analyze entities (extract key topics)
        entities_response = language_client.analyze_entities(
            request={"document": document}
        )
        entities = [entity.name for entity in entities_response.entities[:5]]
        
        # Convert score to our categories
        score = sentiment.score
        magnitude = sentiment.magnitude
        
        if score < -0.25:
            sentiment_label = "frustrated"
            priority = "high"
        elif score > 0.25:
            sentiment_label = "positive"
            priority = "normal"
        else:
            sentiment_label = "neutral"
            priority = "normal"
        
        return {
            "sentiment": sentiment_label,
            "score": score,
            "magnitude": magnitude,
            "priority": priority,
            "key_topics": entities,
            "analysis": f"Sentiment: {sentiment_label} (score: {score:.2f}, magnitude: {magnitude:.2f})"
        }
    except Exception as e:
        return {
            "sentiment": "neutral",
            "error": str(e),
            "priority": "normal"
        }


# ============================================================================
# FILEMANAGER - Real Cloud Storage & Drive
# ============================================================================

def upload_to_cloud_storage(filename: str, content: bytes, auto_organize: bool = True) -> str:
    """Upload file to Google Cloud Storage with smart organization"""
    try:
        bucket = storage_client.bucket("cortex_agent_staging")
        
        # Smart categorization
        category = "general"
        filename_lower = filename.lower()
        
        if any(ext in filename_lower for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
            if "screenshot" in filename_lower:
                category = "screenshots"
            elif any(word in filename_lower for word in ["design", "mockup", "ui", "ux"]):
                category = "designs"
            else:
                category = "images"
        elif any(ext in filename_lower for ext in [".mp4", ".mov", ".avi", ".mkv"]):
            if "zoom" in filename_lower or "meeting" in filename_lower:
                category = "meetings"
            else:
                category = "videos"
        elif any(ext in filename_lower for ext in [".mp3", ".wav", ".m4a", ".flac"]):
            category = "audio"
        elif any(ext in filename_lower for ext in [".py", ".js", ".ts", ".java", ".cpp", ".go"]):
            category = "code"
        elif any(ext in filename_lower for ext in [".md", ".txt", ".doc", ".docx", ".pdf"]):
            if "prompt" in filename_lower:
                category = "prompts"
            else:
                category = "documents"
        
        # Upload to organized path
        blob_path = f"organized/{category}/{datetime.now().strftime('%Y-%m')}/{filename}" if auto_organize else filename
        blob = bucket.blob(blob_path)
        blob.upload_from_string(content)
        
        return f"✅ Uploaded to: gs://cortex_agent_staging/{blob_path}"
    except Exception as e:
        return f"❌ Upload failed: {str(e)}"


def list_files_in_category(category: str = "all", limit: int = 20) -> List[Dict[str, Any]]:
    """List files from Cloud Storage by category"""
    try:
        bucket = storage_client.bucket("cortex_agent_staging")
        
        prefix = f"organized/{category}/" if category != "all" else "organized/"
        blobs = bucket.list_blobs(prefix=prefix, max_results=limit)
        
        files = []
        for blob in blobs:
            files.append({
                "name": blob.name.split("/")[-1],
                "category": blob.name.split("/")[1] if "/" in blob.name else "uncategorized",
                "size": blob.size,
                "created": blob.time_created.isoformat(),
                "url": f"gs://cortex_agent_staging/{blob.name}"
            })
        
        return files
    except Exception as e:
        return [{"error": str(e)}]


# ============================================================================
# VISIONANALYZER - Real Image Analysis
# ============================================================================

def analyze_image_with_vision(image_content: bytes) -> Dict[str, Any]:
    """Use Cloud Vision API for real image analysis"""
    try:
        image = vision.Image(content=image_content)
        
        # Multiple feature detection
        features = [
            vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
            vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
            vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION),
            vision.Feature(type_=vision.Feature.Type.FACE_DETECTION),
        ]
        
        response = vision_client.annotate_image({
            'image': image,
            'features': features
        })
        
        # Extract results
        labels = [label.description for label in response.label_annotations[:10]]
        objects = [obj.name for obj in response.localized_object_annotations[:5]]
        texts = response.text_annotations[0].description if response.text_annotations else ""
        faces_count = len(response.face_annotations)
        
        return {
            "labels": labels,
            "objects": objects,
            "text_detected": texts,
            "faces_count": faces_count,
            "analysis": f"Found {len(labels)} labels, {len(objects)} objects, {faces_count} faces. Text: {texts[:100]}..."
        }
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# MEDIAPROCESSOR - Real Audio/Video Transcription
# ============================================================================

def transcribe_audio_with_speech(audio_content: bytes) -> str:
    """Use Cloud Speech-to-Text API for real transcription"""
    try:
        audio = speech_v1.RecognitionAudio(content=audio_content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long"
        )
        
        response = speech_client.recognize(config=config, audio=audio)
        
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()
    except Exception as e:
        return f"Transcription failed: {str(e)}"


# ============================================================================
# WORKSPACEMANAGER - Real Gmail, Drive, Calendar, Sheets
# ============================================================================

def send_email_with_gmail(to: str, subject: str, body: str) -> str:
    """Send email using Gmail API"""
    try:
        service = get_workspace_service('gmail', 'v1')
        
        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {to}\nSubject: {subject}\n\n{body}".encode()
            ).decode()
        }
        
        service.users().messages().send(userId='me', body=message).execute()
        return f"✅ Email sent to {to}"
    except Exception as e:
        return f"❌ Email failed: {str(e)}"


def list_drive_files(query: str = "", max_results: int = 20) -> List[Dict[str, Any]]:
    """List files from Google Drive"""
    try:
        service = get_workspace_service('drive', 'v3')
        
        results = service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, mimeType, createdTime, modifiedTime)"
        ).execute()
        
        return results.get('files', [])
    except Exception as e:
        return [{"error": str(e)}]


def create_calendar_event(summary: str, start_time: str, end_time: str, description: str = "") -> str:
    """Create event in Google Calendar"""
    try:
        service = get_workspace_service('calendar', 'v3')
        
        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
            'end': {'dateTime': end_time, 'timeZone': 'America/Los_Angeles'},
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Event created: {event.get('htmlLink')}"
    except Exception as e:
        return f"❌ Event creation failed: {str(e)}"


def read_google_sheet(spreadsheet_id: str, range_name: str) -> List[List[Any]]:
    """Read data from Google Sheets"""
    try:
        service = get_workspace_service('sheets', 'v4')
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        return result.get('values', [])
    except Exception as e:
        return [[f"Error: {str(e)}"]]


# ============================================================================
# WEBSEARCHER - Real Web Search
# ============================================================================

def search_web_with_custom_search(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """Use Google Custom Search API for real web search"""
    try:
        service = get_workspace_service('customsearch', 'v1')
        
        # You'll need to set up Custom Search API credentials
        result = service.cse().list(
            q=query,
            cx='YOUR_SEARCH_ENGINE_ID',  # User needs to create this
            num=num_results
        ).execute()
        
        return result.get('items', [])
    except Exception as e:
        return [{"error": str(e)}]


# Export all tools
__all__ = [
    'analyze_sentiment_with_ai',
    'upload_to_cloud_storage',
    'list_files_in_category',
    'analyze_image_with_vision',
    'transcribe_audio_with_speech',
    'send_email_with_gmail',
    'list_drive_files',
    'create_calendar_event',
    'read_google_sheet',
    'search_web_with_custom_search'
]

