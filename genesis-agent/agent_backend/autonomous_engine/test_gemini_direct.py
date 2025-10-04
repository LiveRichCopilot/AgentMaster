"""
Direct test of Gemini API to diagnose the timeout issue
"""

import asyncio
from google import genai
from google.genai import types as genai_types

async def test_gemini_connection():
    """Test if we can connect to Gemini via Vertex AI"""
    
    print("🔍 Testing Gemini connection...")
    print("="*70)
    
    try:
        # Initialize client (same as llm_integration.py)
        print("1. Initializing Gemini client with Vertex AI...")
        client = genai.Client(
            vertexai=True,
            project='studio-2416451423-f2d96',
            location='us-central1'
        )
        print("✅ Client initialized")
        
        # Try a simple API call
        print("\n2. Sending test prompt to Gemini...")
        
        # Set a timeout
        async def call_gemini():
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=[
                    genai_types.Content(
                        role='user',
                        parts=[genai_types.Part.from_text(text="Say 'Hello' in JSON format: {\"message\": \"your response\"}")]
                    )
                ],
                config=genai_types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=100,
                    response_mime_type="application/json"
                )
            )
            return response
        
        # Add timeout
        response = await asyncio.wait_for(call_gemini(), timeout=10.0)
        
        print("✅ Got response from Gemini!")
        print(f"📄 Response: {response.text}")
        
        print("\n" + "="*70)
        print("✅ SUCCESS: Gemini connection works!")
        return True
        
    except asyncio.TimeoutError:
        print("\n" + "="*70)
        print("❌ TIMEOUT: Gemini API call took longer than 10 seconds")
        print("This suggests the API call is hanging/blocking")
        return False
        
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_gemini_connection())
    exit(0 if result else 1)

