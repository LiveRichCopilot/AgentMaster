#!/usr/bin/env python3
"""
Test all 6 core tools in JAi Cortex OS
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
APP_NAME = "jai_cortex"
USER_ID = "diagnostic_test"
SESSION_ID = f"test_{int(time.time())}"

def test_tool(tool_name, message):
    """Test a specific tool by sending a message"""
    print(f"\n{'='*60}")
    print(f"Testing: {tool_name}")
    print(f"{'='*60}")
    
    payload = {
        "appName": APP_NAME,
        "userId": USER_ID,
        "sessionId": SESSION_ID,
        "newMessage": {
            "parts": [{"text": message}]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/run",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {tool_name} - SUCCESS")
            
            # Extract response text
            if 'content' in result and 'parts' in result['content']:
                for part in result['content']['parts']:
                    if 'text' in part:
                        print(f"Response: {part['text'][:200]}...")
                        break
            return True
        else:
            print(f"❌ {tool_name} - FAILED")
            print(f"Status: {response.status_code}")
            print(f"Error: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ {tool_name} - EXCEPTION")
        print(f"Error: {str(e)}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║          JAi CORTEX OS - PHASE 1 TOOL DIAGNOSTICS           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create session first
    print("Creating test session...")
    try:
        session_response = requests.post(
            f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions",
            json={"state": {}}
        )
        if session_response.status_code == 200:
            global SESSION_ID
            SESSION_ID = session_response.json().get('id', SESSION_ID)
            print(f"✅ Session created: {SESSION_ID}\n")
        else:
            print(f"⚠️  Using fallback session ID\n")
    except Exception as e:
        print(f"⚠️  Session creation failed, using fallback: {e}\n")
    
    results = {}
    
    # Test 1: save_note (already confirmed working)
    results['save_note'] = test_tool(
        "save_note",
        "Save this test note with title 'Diagnostic Test' and content 'Testing save functionality'"
    )
    time.sleep(2)
    
    # Test 2: simple_search
    results['simple_search'] = test_tool(
        "simple_search",
        "Search the web for the latest news about Gemini 2.5"
    )
    time.sleep(2)
    
    # Test 3: analyze_image (requires image upload - skip for now)
    print(f"\n{'='*60}")
    print("analyze_image - REQUIRES IMAGE UPLOAD (manual test needed)")
    print(f"{'='*60}")
    results['analyze_image'] = None
    
    # Test 4: extract_text_from_image (requires image upload - skip for now)
    print(f"\n{'='*60}")
    print("extract_text_from_image - REQUIRES IMAGE UPLOAD (manual test needed)")
    print(f"{'='*60}")
    results['extract_text_from_image'] = None
    
    # Test 5: analyze_video (requires video upload - skip for now)
    print(f"\n{'='*60}")
    print("analyze_video - REQUIRES VIDEO UPLOAD (manual test needed)")
    print(f"{'='*60}")
    results['analyze_video'] = None
    
    # Test 6: transcribe_video (requires video upload - skip for now)
    print(f"\n{'='*60}")
    print("transcribe_video - REQUIRES VIDEO UPLOAD (manual test needed)")
    print(f"{'='*60}")
    results['transcribe_video'] = None
    
    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for tool, result in results.items():
        status = "✅ PASS" if result is True else "❌ FAIL" if result is False else "⏭️  SKIP (manual test)"
        print(f"{tool:30s} {status}")
    
    print("\n")

if __name__ == "__main__":
    main()

