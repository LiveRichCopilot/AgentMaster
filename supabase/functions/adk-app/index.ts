import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const htmlContent = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#0a0a0a" />
    <title>LIV - ADK Agent Assistant</title>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background: #0a0a0a;
        color: #ffffff;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
      }
      .header {
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(20, 184, 166, 0.2);
        padding: 1rem 2rem;
      }
      .header h1 {
        color: #14b8a6;
        font-size: 1.5rem;
        font-weight: 600;
      }
      .container {
        flex: 1;
        display: flex;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        padding: 2rem;
        gap: 2rem;
      }
      .chat-panel {
        flex: 1;
        background: rgba(20, 20, 20, 0.6);
        border-radius: 1rem;
        border: 1px solid rgba(20, 184, 166, 0.2);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }
      .messages {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
      }
      .message {
        padding: 1rem;
        border-radius: 0.75rem;
        animation: slideIn 0.3s ease-out;
      }
      @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .message.user {
        background: rgba(20, 184, 166, 0.2);
        border: 1px solid rgba(20, 184, 166, 0.3);
        align-self: flex-end;
        max-width: 80%;
      }
      .message.assistant {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        align-self: flex-start;
        max-width: 80%;
      }
      .input-area {
        padding: 1.5rem;
        background: rgba(10, 10, 10, 0.8);
        border-top: 1px solid rgba(20, 184, 166, 0.2);
      }
      .input-container {
        display: flex;
        gap: 1rem;
      }
      input {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        color: white;
        font-size: 1rem;
      }
      input:focus {
        outline: none;
        border-color: #14b8a6;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
      }
      button {
        background: #14b8a6;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
      }
      button:hover {
        background: #0d9488;
        transform: translateY(-1px);
      }
      button:active {
        transform: translateY(0);
      }
      button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      .welcome {
        text-align: center;
        padding: 3rem;
        color: rgba(255, 255, 255, 0.6);
      }
      .welcome h2 {
        color: #14b8a6;
        margin-bottom: 1rem;
      }
      .status {
        position: fixed;
        top: 1rem;
        right: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        z-index: 1000;
      }
      .status.connected {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #10b981;
      }
      .status.disconnected {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #ef4444;
      }
    </style>
  </head>
  <body>
    <div class="status disconnected" id="status">Connecting...</div>
    <div class="header">
      <h1>🤖 LIV - ADK Agent Assistant</h1>
    </div>
    <div class="container">
      <div class="chat-panel">
        <div class="messages" id="messages">
          <div class="welcome">
            <h2>Welcome to LIV Agent</h2>
            <p>Your powerful ADK agent is ready to help. Start chatting below!</p>
          </div>
        </div>
        <div class="input-area">
          <div class="input-container">
            <input type="text" id="input" placeholder="Type your message..." />
            <button id="send">Send</button>
          </div>
        </div>
      </div>
    </div>
    <script>
      const messages = document.getElementById('messages');
      const input = document.getElementById('input');
      const send = document.getElementById('send');
      const status = document.getElementById('status');

      const AGENT_URL = 'http://127.0.0.1:8000';

      async function checkConnection() {
        try {
          const response = await fetch(AGENT_URL + '/health', { method: 'GET' });
          if (response.ok) {
            status.textContent = 'Connected';
            status.className = 'status connected';
            return true;
          }
        } catch (e) {
          status.textContent = 'Agent Offline';
          status.className = 'status disconnected';
          return false;
        }
      }

      function addMessage(text, isUser) {
        const welcome = messages.querySelector('.welcome');
        if (welcome) welcome.remove();

        const msg = document.createElement('div');
        msg.className = 'message ' + (isUser ? 'user' : 'assistant');
        msg.textContent = text;
        messages.appendChild(msg);
        messages.scrollTop = messages.scrollHeight;
      }

      async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        input.value = '';
        addMessage(text, true);
        send.disabled = true;

        try {
          const response = await fetch(AGENT_URL + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
          });

          const data = await response.json();
          addMessage(data.response || 'No response received', false);
        } catch (error) {
          addMessage('Error: Could not connect to agent. Make sure your ADK agent is running on port 8000.', false);
        } finally {
          send.disabled = false;
          input.focus();
        }
      }

      send.addEventListener('click', sendMessage);
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
      });

      checkConnection();
      setInterval(checkConnection, 5000);
    </script>
  </body>
</html>`;

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  return new Response(htmlContent, {
    headers: {
      ...corsHeaders,
      "Content-Type": "text/html",
    },
  });
});
