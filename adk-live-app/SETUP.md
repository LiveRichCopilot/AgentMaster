# Quick Setup Guide

## 1. Start your ADK Agent

Make sure your ADK agent is running on `http://127.0.0.1:8000` with these API endpoints:

```python
# Example ADK endpoints needed:
@app.post("/api/chat")
async def chat(request: dict):
    # Handle chat message
    return {"response": "Hello from agent"}

@app.post("/api/execute")
async def execute_code(request: dict):
    # Execute code and return output
    return {"output": "code result", "error": None}

@app.get("/api/sessions")
async def get_sessions():
    # Return session history
    return []

@app.websocket("/api/stream")
async def websocket_stream(websocket):
    # Real-time streaming responses
    pass
```

## 2. Install & Run the Web App

```bash
# In the adk-live-app directory
npm install
npm run dev
```

## 3. Open Your Browser

Navigate to the URL shown (usually `http://localhost:5173`)

## 4. Features to Try

### Voice Chat
1. Click the microphone icon in the header to enable voice mode
2. Click the large microphone button to start speaking
3. LIV will transcribe your speech and respond with voice

### Code Editor
1. Click the "Live Editor" card on the home screen
2. Write Python or TypeScript code
3. Click "Run Code" to execute via your ADK agent

### Chat Interface
1. Type messages in the input field at the bottom
2. Press Enter to send (Shift+Enter for new line)
3. Click the sidebar icon to view session history

## Troubleshooting

### Voice not working?
- Use Chrome or Edge browsers for full voice support
- Allow microphone permissions when prompted
- Check browser console for errors

### Can't connect to ADK?
- Verify your agent is running on `http://127.0.0.1:8000`
- Check CORS settings on your agent (allow all origins for local dev)
- Open browser console to see connection errors

### Build errors?
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

## Production Deployment

```bash
npm run build
```

Serve the `dist/` folder with any static file server:
```bash
npx serve dist
```

Or deploy to Vercel/Netlify/Firebase Hosting.
