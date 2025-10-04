"""
Media Processing Tools
Handle video/audio uploads, transcription, analysis
"""

import os
import base64
from typing import Dict, Any
from pathlib import Path
from datetime import datetime

# Try to import Google Cloud libs
try:
    from google.cloud import videointelligence_v1 as videointelligence
    from google.cloud import speech_v1 as speech
    from google.cloud import storage
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    HAS_MEDIA_LIBS = True
except:
    HAS_MEDIA_LIBS = False

MEDIA_DIR = Path(__file__).parent / "media_uploads"
MEDIA_DIR.mkdir(exist_ok=True)

GCS_BUCKET = "studio-2416451423-f2d96.firebasestorage.app"
PROJECT_ID = "studio-2416451423-f2d96"

# ============================================================================
# VIDEO PROCESSING
# ============================================================================

def upload_zoom_video_impl(video_base64: str, filename: str) -> Dict[str, Any]:
    """Upload a Zoom video for processing"""
    try:
        # Decode and save locally
        video_data = base64.b64decode(video_base64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_filename = filename.replace('.mp4', '') + f"_{timestamp}.mp4"
        local_path = MEDIA_DIR / clean_filename
        
        with open(local_path, 'wb') as f:
            f.write(video_data)
        
        # Upload to GCS
        if HAS_MEDIA_LIBS:
            storage_client = storage.Client()
            bucket = storage_client.bucket(GCS_BUCKET)
            blob = bucket.blob(f"zoom_videos/{clean_filename}")
            blob.upload_from_filename(str(local_path))
            gcs_uri = f"gs://{GCS_BUCKET}/zoom_videos/{clean_filename}"
        else:
            gcs_uri = None
        
        return {
            'status': 'success',
            'message': 'Video uploaded successfully',
            'filename': clean_filename,
            'local_path': str(local_path),
            'gcs_uri': gcs_uri,
            'size_mb': round(len(video_data) / 1024 / 1024, 2)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def transcribe_video_impl(gcs_uri: str) -> Dict[str, Any]:
    """Transcribe video using Speech-to-Text"""
    if not HAS_MEDIA_LIBS:
        return {'status': 'error', 'message': 'Media libraries not available'}
    
    try:
        # Use Video Intelligence API for transcription
        video_client = videointelligence.VideoIntelligenceServiceClient()
        
        features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]
        
        config = videointelligence.SpeechTranscriptionConfig(
            language_code="en-US",
            enable_automatic_punctuation=True,
            enable_word_time_offsets=True
        )
        
        context = videointelligence.VideoContext(
            speech_transcription_config=config
        )
        
        operation = video_client.annotate_video(
            request={
                "features": features,
                "input_uri": gcs_uri,
                "video_context": context
            }
        )
        
        # This is async - in production, you'd poll or use callbacks
        result = operation.result(timeout=300)  # 5 min max
        
        # Extract transcription
        transcript = ""
        for annotation_result in result.annotation_results:
            for speech_transcription in annotation_result.speech_transcriptions:
                for alternative in speech_transcription.alternatives:
                    transcript += alternative.transcript + " "
        
        return {
            'status': 'success',
            'transcript': transcript.strip(),
            'gcs_uri': gcs_uri
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def analyze_video_content_impl(gcs_uri: str, transcript: str) -> Dict[str, Any]:
    """Analyze video content with Gemini"""
    if not HAS_MEDIA_LIBS:
        return {'status': 'error', 'message': 'Media libraries not available'}
    
    try:
        vertexai.init(project=PROJECT_ID, location="us-central1")
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        prompt = f"""
Analyze this meeting transcript and extract:

1. KEY TOPICS (top 3-5 main discussion points)
2. ACTION ITEMS (who needs to do what)
3. DECISIONS MADE (what was decided)
4. IMPORTANT DATES/DEADLINES mentioned
5. SENTIMENT (overall tone: positive/neutral/negative)
6. SUGGESTED LABEL (1-3 word category for this meeting)

TRANSCRIPT:
{transcript}

Return as JSON.
"""
        
        response = model.generate_content(prompt)
        
        return {
            'status': 'success',
            'analysis': response.text,
            'gcs_uri': gcs_uri
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def auto_label_video_impl(analysis: str) -> Dict[str, Any]:
    """Auto-generate labels and organization from analysis"""
    try:
        # Extract suggested label from analysis
        # In production, parse the JSON response
        
        # For now, return a structured label
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        return {
            'status': 'success',
            'suggested_filename': f"Meeting_{timestamp}",
            'tags': ['meeting', 'zoom', timestamp],
            'category': 'Meetings',
            'priority': 'medium'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def extract_highlights_impl(transcript: str, analysis: str) -> Dict[str, Any]:
    """Extract key moments and highlights"""
    try:
        highlights = []
        
        # Look for action items
        if 'action' in analysis.lower():
            highlights.append({
                'type': 'action_item',
                'timestamp': '00:00',  # Would need word timestamps
                'content': 'Action items discussed'
            })
        
        # Look for decisions
        if 'decision' in analysis.lower():
            highlights.append({
                'type': 'decision',
                'timestamp': '00:00',
                'content': 'Important decision made'
            })
        
        return {
            'status': 'success',
            'highlights': highlights,
            'count': len(highlights)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# FULL VIDEO PROCESSING PIPELINE
# ============================================================================

def process_zoom_video_full_impl(video_base64: str, filename: str) -> Dict[str, Any]:
    """
    Full pipeline: Upload → Transcribe → Analyze → Label → Extract Highlights
    """
    try:
        # Step 1: Upload
        upload_result = upload_zoom_video_impl(video_base64, filename)
        if upload_result['status'] != 'success':
            return upload_result
        
        gcs_uri = upload_result.get('gcs_uri')
        if not gcs_uri:
            return {
                'status': 'partial',
                'message': 'Video saved locally but GCS upload failed',
                'local_path': upload_result['local_path']
            }
        
        # Step 2: Transcribe
        transcribe_result = transcribe_video_impl(gcs_uri)
        if transcribe_result['status'] != 'success':
            return {
                'status': 'partial',
                'message': 'Video uploaded but transcription failed',
                **upload_result
            }
        
        transcript = transcribe_result['transcript']
        
        # Step 3: Analyze
        analysis_result = analyze_video_content_impl(gcs_uri, transcript)
        if analysis_result['status'] != 'success':
            return {
                'status': 'partial',
                'message': 'Transcription complete but analysis failed',
                'transcript': transcript,
                **upload_result
            }
        
        analysis = analysis_result['analysis']
        
        # Step 4: Auto-label
        label_result = auto_label_video_impl(analysis)
        
        # Step 5: Extract highlights
        highlights_result = extract_highlights_impl(transcript, analysis)
        
        return {
            'status': 'success',
            'message': 'Full video processing complete',
            'filename': upload_result['filename'],
            'gcs_uri': gcs_uri,
            'transcript': transcript,
            'analysis': analysis,
            'labels': label_result,
            'highlights': highlights_result.get('highlights', []),
            'size_mb': upload_result['size_mb']
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
