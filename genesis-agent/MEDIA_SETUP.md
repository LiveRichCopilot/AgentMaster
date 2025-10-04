# Media Processing Setup Guide

## System Dependencies Required

### 1. FFmpeg (Video/Audio Processing)
```bash
brew install ffmpeg
```
**Provides:**
- `ffmpeg` - Video/audio conversion, extraction, manipulation
- `ffprobe` - Video metadata analysis

### 2. Python Packages (Already in requirements.txt)
```
google-cloud-videointelligence==2.13.5  # Video analysis
google-cloud-speech==2.28.0              # Audio transcription
google-cloud-storage==2.18.2             # File storage
```

### 3. Optional: OpenCV (Frame Extraction)
```bash
pip install opencv-python
```

## What Each Tool Needs

### `analyze_video` 
- ✅ Needs: `ffprobe` (from ffmpeg)
- Extracts: metadata, duration, resolution, codec info

### `extract_audio_from_video`
- ✅ Needs: `ffmpeg`
- Extracts: audio track as WAV file

### `transcribe_video`
- ✅ Needs: `ffmpeg` + `google-cloud-speech`
- Extracts audio, then transcribes it

### `analyze_image` / `extract_text_from_image`
- ✅ Needs: `google-cloud-vision` (already installed)
- OCR and image analysis

### `call_media_processor` (Deployed Agent)
- ✅ Needs: MediaProcessor agent deployed to Vertex AI
- Advanced processing capabilities

## Installation Steps

```bash
# 1. Install ffmpeg (macOS)
brew install ffmpeg

# 2. Verify installation
ffmpeg -version
ffprobe -version

# 3. Optional: Install OpenCV for frame extraction
pip install opencv-python

# 4. Test
python -c "import subprocess; subprocess.run(['ffmpeg', '-version'])"
```

## Current Status
- ❌ ffmpeg NOT installed → Installing now
- ✅ Python packages installed
- ❌ MediaProcessor agent needs authentication fix (401 error)

