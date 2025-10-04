"""
Streaming Voice - Real-time bidirectional audio with Vertex AI Live API
"""

import asyncio
import base64
from typing import AsyncIterator, Dict, Any
from vertexai.generative_models import GenerativeModel, Part, Content
import vertexai

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Use Gemini 2.0 Flash Exp for live audio streaming
live_model = GenerativeModel("gemini-2.0-flash-exp")

async def stream_voice_chat(
    audio_chunks: AsyncIterator[bytes],
    session_history: list = None
) -> AsyncIterator[Dict[str, Any]]:
    """
    Stream audio bidirectionally with Gemini Live API
    
    Args:
        audio_chunks: Async iterator of audio bytes (WebRTC/mic input)
        session_history: Previous conversation history
        
    Yields:
        Dict with 'type' (audio/text/tool) and 'data'
    """
    
    # Start live session
    chat = live_model.start_chat(history=session_history or [])
    
    # Process incoming audio chunks
    async for audio_chunk in audio_chunks:
        # Send audio to model
        audio_part = Part.from_data(data=audio_chunk, mime_type="audio/pcm")
        
        try:
            # Get streaming response
            response_stream = chat.send_message_async(audio_part, stream=True)
            
            async for response_chunk in response_stream:
                # Check response type
                if response_chunk.candidates:
                    for part in response_chunk.candidates[0].content.parts:
                        # Audio response
                        if hasattr(part, 'inline_data') and part.inline_data:
                            if part.inline_data.mime_type.startswith('audio/'):
                                yield {
                                    'type': 'audio',
                                    'data': base64.b64encode(part.inline_data.data).decode(),
                                    'mime_type': part.inline_data.mime_type
                                }
                        
                        # Text response
                        if hasattr(part, 'text') and part.text:
                            yield {
                                'type': 'text',
                                'data': part.text
                            }
                        
                        # Function call
                        if hasattr(part, 'function_call') and part.function_call:
                            yield {
                                'type': 'tool',
                                'data': {
                                    'name': part.function_call.name,
                                    'args': dict(part.function_call.args)
                                }
                            }
        
        except Exception as e:
            yield {
                'type': 'error',
                'data': str(e)
            }


async def simple_voice_response(audio_base64: str) -> Dict[str, Any]:
    """
    Simple voice-to-voice response (non-streaming)
    
    Args:
        audio_base64: Base64 encoded audio
        
    Returns:
        Dict with text and audio response
    """
    try:
        # Decode audio
        audio_data = base64.b64decode(audio_base64)
        
        # Send to model
        audio_part = Part.from_data(data=audio_data, mime_type="audio/pcm")
        response = live_model.generate_content(audio_part)
        
        # Extract response
        text_response = ""
        audio_response = None
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                text_response += part.text
            
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type.startswith('audio/'):
                    audio_response = base64.b64encode(part.inline_data.data).decode()
        
        return {
            'status': 'success',
            'text': text_response,
            'audio': audio_response,
            'note': 'Use WebSocket for real-time streaming'
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


