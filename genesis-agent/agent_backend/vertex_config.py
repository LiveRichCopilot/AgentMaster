"""
Vertex AI Configuration - MUST be imported FIRST before any google modules
"""

import os
import sys

# Set Vertex AI environment BEFORE any google imports
os.environ['GOOGLE_CLOUD_PROJECT'] = 'studio-2416451423-f2d96'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

# Explicitly configure genai to use Vertex AI
def configure_vertex_ai():
    """Configure google-genai to use Vertex AI instead of API key"""
    from google import genai
    from google.genai import Client
    
    # Create a Vertex AI client
    client = Client(
        vertexai=True,
        project='studio-2416451423-f2d96',
        location='us-central1'
    )
    
    # Monkey-patch the default client if needed
    genai._default_client = client
    
    print("✅ Configured google-genai to use Vertex AI")
    print(f"📍 Project: studio-2416451423-f2d96")
    print(f"📍 Location: us-central1")
    
    return client

# Auto-configure on import
configure_vertex_ai()


