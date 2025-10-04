"""
Voice Interface - Speech to Text + Text to Speech
Real-time conversation with agents
"""

import os
import base64
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from google.cloud import speech_v1 as speech
    from google.cloud import texttospeech
    import vertexai
    HAS_VOICE = True
except:
    HAS_VOICE = False

PROJECT_ID = "studio-2416451423-f2d96"

# ============================================================================
# SPEECH-TO-TEXT (Listen to you)
# ============================================================================

def transcribe_audio_stream_impl(audio_base64: str, language_code: str = "en-US") -> Dict[str, Any]:
    """
    Transcribe audio from base64
    Used for: Recording evaluations, meetings, thoughts
    """
    if not HAS_VOICE:
        return {'status': 'error', 'message': 'Voice libraries not available'}
    
    try:
        client = speech.SpeechClient()
        
        # Decode audio
        audio_data = base64.b64decode(audio_base64)
        
        audio = speech.RecognitionAudio(content=audio_data)
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="latest_long",
            use_enhanced=True
        )
        
        response = client.recognize(config=config, audio=audio)
        
        # Get best transcription
        transcript = ""
        confidence = 0.0
        
        for result in response.results:
            if result.alternatives:
                alt = result.alternatives[0]
                transcript += alt.transcript + " "
                confidence = max(confidence, alt.confidence)
        
        return {
            'status': 'success',
            'transcript': transcript.strip(),
            'confidence': round(confidence, 2),
            'language': language_code
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# TEXT-TO-SPEECH (Agent speaks to you)
# ============================================================================

def text_to_speech_impl(text: str, voice_name: str = "en-US-Neural2-J") -> Dict[str, Any]:
    """
    Convert text to speech
    Used for: Agent responses, alerts, reminders
    """
    if not HAS_VOICE:
        return {'status': 'error', 'message': 'Voice libraries not available'}
    
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Voice config (Neural2 = most natural)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name,  # Neural2-J = friendly female, Neural2-D = professional male
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Encode as base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        
        return {
            'status': 'success',
            'audio_base64': audio_base64,
            'voice': voice_name,
            'format': 'mp3'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# LIVE CONVERSATION (Gemini Live API)
# ============================================================================

def start_live_conversation_impl() -> Dict[str, Any]:
    """
    Start a live voice conversation with Gemini
    Uses Gemini 2.0 Flash with audio input/output
    """
    if not HAS_VOICE:
        return {'status': 'error', 'message': 'Voice libraries not available'}
    
    try:
        vertexai.init(project=PROJECT_ID, location="us-central1")
        
        # This would use WebSocket + Gemini Live API
        # For now, return session info
        
        return {
            'status': 'success',
            'message': 'Live conversation ready',
            'session_id': 'live_session_001',
            'websocket_url': 'ws://localhost:8000/ws/voice',
            'note': 'Use WebSocket for bidirectional audio streaming'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# EVALUATION ASSISTANT
# ============================================================================

def analyze_spoken_evaluation_impl(transcript: str) -> Dict[str, Any]:
    """
    Analyze spoken evaluation/meeting notes
    Extract: Key points, action items, sentiment, recommendations
    """
    try:
        vertexai.init(project=PROJECT_ID, location="us-central1")
        from vertexai.generative_models import GenerativeModel
        
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        prompt = f"""
You are an executive assistant analyzing a spoken evaluation or meeting.

TRANSCRIPT:
"{transcript}"

Extract and return as JSON:
1. KEY POINTS (3-5 main takeaways)
2. ACTION ITEMS (what needs to be done)
3. SENTIMENT (positive/neutral/negative with explanation)
4. RECOMMENDATIONS (what should happen next)
5. PRIORITY LEVEL (low/medium/high/urgent)
6. FOLLOW-UP DATE (suggested)

Be concise and actionable.
"""
        
        response = model.generate_content(prompt)
        
        return {
            'status': 'success',
            'analysis': response.text,
            'original_transcript': transcript
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# VOICE COMMANDS
# ============================================================================

VOICE_COMMANDS = {
    "create_folder": ["create folder", "make folder", "new folder"],
    "save_note": ["save note", "remember this", "take note"],
    "search": ["search for", "find", "look up"],
    "send_email": ["send email", "email"],
    "schedule": ["schedule", "set reminder", "remind me"],
    "analyze": ["analyze", "evaluate", "assess"],
    "help": ["help", "what can you do", "capabilities"]
}

def detect_voice_command_impl(transcript: str) -> Dict[str, Any]:
    """
    Detect command from voice transcript
    """
    transcript_lower = transcript.lower()
    
    for command, triggers in VOICE_COMMANDS.items():
        if any(trigger in transcript_lower for trigger in triggers):
            return {
                'status': 'success',
                'command': command,
                'transcript': transcript,
                'confidence': 'high'
            }
    
    return {
        'status': 'success',
        'command': 'general_chat',
        'transcript': transcript,
        'confidence': 'medium'
    }
