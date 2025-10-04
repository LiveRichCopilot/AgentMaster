# Genesis Agent 🤖

The most advanced AI agent architect that **builds, deploys, and manages intelligent agent systems**. Genesis Agent doesn't just suggest configurations - it can create agents that build other agents, deploy themselves, monitor their own health, and continuously self-improve.

## Revolutionary Features ⚡

### Core Capabilities
- 🎨 **Beautiful Apple glassmorphic design** with animated gradients
- 💬 **Real-time chat interface** with advanced AI responses
- 🔧 **Task Automation & Workflows** - Multi-step execution
- 🌐 **Web Search & API Integration** - Live internet access
- ☁️ **Full Firebase/GCP Integration** - All Google Cloud services
- 🤖 **AI & ML Tools** - Gemini, Vision, Speech, Translation

### Meta-Tools (Self-Managing Capabilities)
- 🏗️ **Agent Scaffolding** - Generates new sub-agents automatically
- 🚀 **Auto-Deployment** - Executes gcloud/firebase CLI commands
- 📊 **System Monitoring** - Reads logs, tracks metrics, detects issues
- 🩺 **Self-Correction** - Analyzes failures and auto-fixes code
- 💻 **Code Generation** - Creates Cloud Functions, APIs, schemas
- 🔄 **Version Control** - Git operations for agent evolution

## Design

- **Black gradient background** with animated pink, turquoise, and turquoise-green orbs
- **Glassmorphic UI** with blur effects and semi-transparent elements
- **Rounded corners** everywhere (rounded-xl and above)
- **SF Pro Display** font family for that Apple aesthetic
- **Pink & Turquoise** color scheme with smooth gradients

## Setup 🚀

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Add your Gemini API Key:**
   
   Edit the `.env` file and add your API key:
   ```
   VITE_GEMINI_API_KEY=your_api_key_here
   ```
   
   Get your API key from: https://makersuite.google.com/app/apikey

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

5. **Deploy to Firebase:**
   ```bash
   firebase login
   firebase deploy
   ```

## Firebase Configuration

The app is configured to use Firebase project: `studio-2416451423-f2d96`

Firebase config is already set up in `src/firebase.js`

## Tech Stack 💻

- **React** - UI framework
- **Vite** - Build tool
- **Firebase** - Backend & hosting
- **Google Gemini AI** - AI model (gemini-2.0-flash-exp)
- **CSS3** - Custom glassmorphic styling

## Project Structure

```
genesis-agent/
├── src/
│   ├── App.jsx          # Main application component
│   ├── App.css          # Glassmorphic styles
│   ├── firebase.js      # Firebase configuration
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── firebase.json        # Firebase hosting config
├── .firebaserc          # Firebase project config
└── .env                 # Environment variables
```

## What Makes Genesis Agent Revolutionary 🌟

### Traditional AI Agents
- Respond to prompts ✓
- Access APIs ✓
- Generate text ✓

### Genesis Agent
- **Builds other agents** ✓
- **Deploys them to the cloud** ✓
- **Monitors their performance** ✓
- **Fixes their own bugs** ✓
- **Continuously improves** ✓
- **Creates entire agent ecosystems** ✓

## Example Use Cases 💡

### 1. "Create a customer support system"
Genesis Agent will:
- Design a multi-agent architecture
- Generate 5 specialized sub-agents (triage, FAQ, escalation, analytics, feedback)
- Scaffold all the code
- Deploy to Firebase/GCP
- Set up monitoring and auto-healing
- Provide a complete working system in minutes

### 2. "Build an e-commerce automation platform"
Genesis Agent will:
- Create agents for: inventory, pricing, marketing, customer service
- Set up workflows: order processing, email campaigns, stock alerts
- Integrate with: Stripe, SendGrid, analytics tools
- Deploy everything and start monitoring
- Auto-optimize based on performance data

### 3. "I need a DevOps agent that manages my microservices"
Genesis Agent will:
- Create a self-managing orchestrator agent
- Build sub-agents for: deployment, monitoring, logging, optimization
- Set up auto-healing (detects errors → reads logs → fixes code → redeploys)
- Implement A/B testing for performance optimization
- Provide cost monitoring and optimization

## How to Use 🚀

1. **Describe what you want to build**
2. **Genesis Agent analyzes your needs**
3. **Provides complete configuration** with:
   - Agent architecture (including sub-agents if needed)
   - JSON configuration files
   - Recommended Firebase/GCP services
   - Deployment strategy
   - Self-improvement plan
4. **Optionally: Genesis can deploy it for you** (with meta-tools enabled)

## Available Commands

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
firebase deploy      # Deploy to Firebase Hosting
```

## License

MIT

---

Built with ❤️ using React, Firebase, and Gemini AI