# LIV - ADK Agent Assistant

A beautiful glassmorphic web app with Apple iOS 26 Liquid Glass aesthetic that connects to your ADK agents.

## Features

- **Voice Chat with LIV** - Talk to your agent using Web Speech API with text-to-speech responses
- **Live Code Editor** - Monaco Editor with syntax highlighting and live execution
- **Glassmorphic UI** - Black background with teal accents and smooth animations
- **Real-time Communication** - WebSocket connection to ADK agents
- **Session Management** - Track and manage conversation history
- **Mobile Responsive** - Works beautifully on all devices

## Tech Stack

- React + TypeScript + Vite
- Tailwind CSS for styling
- Monaco Editor for code editing
- Web Speech API for voice
- WebSocket for real-time communication
- Framer Motion for animations

## Setup

1. Install dependencies:
```bash
npm install
```

2. Make sure your ADK agent is running on `http://127.0.0.1:8000`

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to the URL shown in the terminal

## API Endpoints Required

Your ADK agent should expose these endpoints:

- `POST /api/chat` - Send messages to the agent
- `POST /api/execute` - Execute code
- `WS /api/stream` - WebSocket for real-time responses
- `GET /api/sessions` - Get chat history

## Voice Features

- Click the microphone button to start voice recognition
- Speak naturally - LIV will transcribe in real-time
- Stops automatically after 2 seconds of silence
- LIV responds with voice when voice mode is enabled
- Works best in Chrome and Edge browsers

## Code Editor

- Write Python or TypeScript code
- Click "Run Code" to execute via your ADK agent
- View output or errors in the preview panel
- Toggle preview panel visibility

## Build for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

## Browser Compatibility

- Chrome/Edge: Full support including voice features
- Firefox/Safari: Limited voice support
- All modern browsers support the core chat and code features
