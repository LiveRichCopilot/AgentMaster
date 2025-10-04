"""
Screen Capture and Vision Tools
"""

import os
import base64
import subprocess
from typing import Dict, Any
from pathlib import Path
from datetime import datetime

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

def capture_screen_impl() -> Dict[str, Any]:
    """Capture screenshot of entire screen"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        # Use macOS screencapture
        result = subprocess.run(
            ['screencapture', '-x', str(filepath)],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return {'status': 'error', 'message': 'Screenshot failed'}
        
        # Read and encode
        with open(filepath, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        
        return {
            'status': 'success',
            'message': 'Screenshot captured',
            'filename': filename,
            'path': str(filepath),
            'image_base64': image_data
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def capture_window_impl(app_name: str) -> Dict[str, Any]:
    """Capture screenshot of specific window"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"window_{app_name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        # Use macOS screencapture with window flag
        result = subprocess.run(
            ['screencapture', '-l', '$(osascript -e \'tell app "' + app_name + '" to id of window 1\')', str(filepath)],
            shell=True,
            capture_output=True,
            timeout=5
        )
        
        if not filepath.exists():
            # Fallback to full screen
            return capture_screen_impl()
        
        with open(filepath, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        
        return {
            'status': 'success',
            'message': f'Window screenshot captured: {app_name}',
            'filename': filename,
            'path': str(filepath),
            'image_base64': image_data
        }
    except Exception as e:
        return capture_screen_impl()  # Fallback


def analyze_screenshot_impl(image_base64: str, question: str = "What do you see?") -> Dict[str, Any]:
    """Analyze screenshot with Gemini Vision"""
    try:
        from vertexai.generative_models import GenerativeModel, Part
        import vertexai
        
        vertexai.init(project="studio-2416451423-f2d96", location="us-central1")
        vision_model = GenerativeModel("gemini-2.0-flash-exp")
        
        # Decode image
        image_data = base64.b64decode(image_base64)
        
        # Create parts
        image_part = Part.from_data(data=image_data, mime_type="image/png")
        text_part = Part.from_text(question)
        
        # Analyze
        response = vision_model.generate_content([image_part, text_part])
        
        return {
            'status': 'success',
            'analysis': response.text,
            'question': question
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def list_screenshots_impl() -> Dict[str, Any]:
    """List all captured screenshots"""
    try:
        screenshots = []
        for file in SCREENSHOTS_DIR.glob("*.png"):
            screenshots.append({
                'filename': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
        
        return {
            'status': 'success',
            'count': len(screenshots),
            'screenshots': sorted(screenshots, key=lambda x: x['modified'], reverse=True)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


