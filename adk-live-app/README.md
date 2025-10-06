# Claude Agent - Glassmorphic Coding Assistant

A beautiful, glassmorphic web interface for interacting with Claude AI. Built with React, TypeScript, and Tailwind CSS, featuring real-time streaming responses, code syntax highlighting, voice integration, and persistent sessions.

## Features

### Core Features
- **Real-time Chat with Claude** - Streaming responses with typing indicators
- **Code Syntax Highlighting** - Beautiful code blocks with copy functionality
- **Session Management** - Save and restore conversations in Supabase
- **Voice Integration** - Speech-to-text input and text-to-speech output
- **Live Code Editor** - Monaco editor with syntax highlighting
- **Settings Panel** - Configure model, temperature, max tokens, and system prompt
- **Status Bar** - Real-time connection status, token usage, and model info

### Design
- **Apple iOS 18 Liquid Glass Style** - Modern glassmorphic design
- **Dark Theme** - Black background (#0a0a0a) with teal accents (#14b8a6)
- **Smooth Animations** - Framer Motion powered transitions
- **Responsive Layout** - Works on desktop, tablet, and mobile

### Technical Stack
- **React 19** - Latest React with hooks
- **TypeScript** - Type-safe code
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Monaco Editor** - VS Code's editor component
- **Anthropic SDK** - Official Claude API integration
- **Supabase** - Database and real-time features
- **Zustand** - Simple state management
- **Framer Motion** - Smooth animations

## Getting Started

### Prerequisites
- Node.js 18+
- Claude API key from [console.anthropic.com](https://console.anthropic.com)
- Supabase project (free tier works great)

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Supabase URL and anon key
   ```
   VITE_SUPABASE_URL=your_supabase_project_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. **Start the development server:**
```bash
npm run dev
```

4. **Open the app:**
   - Navigate to `http://localhost:5173`
   - Click "Set API Key" and enter your Claude API key
   - Start chatting!

### Building for Production

```bash
npm run build
```

## Usage

### Setting Up
1. Launch the app
2. Click the settings icon (gear) in the header
3. Enter your Claude API key
4. (Optional) Adjust model, temperature, and other settings

### Chatting with Claude
- Type your message in the input field
- Press Enter or click Send
- Watch Claude's response stream in real-time
- Code blocks are automatically highlighted

### Voice Chat
1. Click the microphone icon to enable voice
2. Click the voice button to start listening
3. Speak your message
4. Claude's response will be read aloud

### Sessions
- Conversations are automatically saved
- Click the sidebar to view past sessions
- Click "New Session" to start fresh

## Architecture

### Project Structure
```
src/
├── components/         # React components
├── services/           # Claude API, Supabase, Voice
├── store/             # Zustand state management
├── types/             # TypeScript interfaces
└── App.tsx            # Main application
```

## Browser Support

- **Recommended**: Chrome, Edge (best voice support)
- **Supported**: Firefox, Safari
- **Speech Recognition**: Chrome/Edge only

## License

MIT License

---

Built with Claude 3.5 Sonnet
