import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

Deno.serve((req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude Agent - Glassmorphic AI Assistant</title>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-typescript.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .glass {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .header {
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .logo {
      font-size: 1.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .btn {
      padding: 0.5rem 1rem;
      border-radius: 0.75rem;
      border: none;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;
    }
    .btn-primary {
      background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
      color: white;
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 15px rgba(20, 184, 166, 0.4);
    }
    .btn-glass {
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .btn-glass:hover {
      background: rgba(255, 255, 255, 0.15);
    }
    .container {
      flex: 1;
      display: flex;
      max-width: 1200px;
      margin: 0 auto;
      width: 100%;
      padding: 2rem;
      gap: 1.5rem;
    }
    .sidebar {
      width: 280px;
      padding: 1.5rem;
      border-radius: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .session-item {
      padding: 0.75rem;
      border-radius: 0.75rem;
      cursor: pointer;
      transition: all 0.2s;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid transparent;
    }
    .session-item:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(20, 184, 166, 0.3);
    }
    .session-item.active {
      background: rgba(20, 184, 166, 0.2);
      border-color: rgba(20, 184, 166, 0.5);
    }
    .chat-panel {
      flex: 1;
      border-radius: 1.5rem;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .messages {
      flex: 1;
      overflow-y: auto;
      padding: 2rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .message {
      display: flex;
      gap: 0.75rem;
      animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .message.user {
      flex-direction: row-reverse;
    }
    .avatar {
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      font-weight: 700;
    }
    .user .avatar {
      background: rgba(255, 255, 255, 0.1);
    }
    .assistant .avatar {
      background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
    }
    .bubble {
      max-width: 70%;
      padding: 1rem 1.5rem;
      border-radius: 1.5rem;
      line-height: 1.6;
    }
    .user .bubble {
      background: linear-gradient(135deg, rgba(20, 184, 166, 0.3) 0%, rgba(13, 148, 136, 0.2) 100%);
      border: 1px solid rgba(20, 184, 166, 0.3);
    }
    .assistant .bubble {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .code-block {
      margin: 0.5rem 0;
      border-radius: 0.75rem;
      overflow: hidden;
    }
    .code-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: rgba(0, 0, 0, 0.4);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .code-lang {
      color: #14b8a6;
      font-size: 0.875rem;
      font-weight: 600;
      text-transform: uppercase;
    }
    .copy-btn {
      padding: 0.25rem 0.75rem;
      border-radius: 0.5rem;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: none;
      cursor: pointer;
      font-size: 0.75rem;
    }
    .copy-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    .input-area {
      padding: 1.5rem;
      background: rgba(10, 10, 20, 0.9);
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .input-container {
      display: flex;
      gap: 1rem;
    }
    input {
      flex: 1;
      padding: 1rem 1.5rem;
      border-radius: 1rem;
      border: none;
      background: rgba(255, 255, 255, 0.05);
      color: white;
      font-size: 1rem;
    }
    input:focus {
      outline: none;
      background: rgba(255, 255, 255, 0.08);
      box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.3);
    }
    .welcome {
      text-align: center;
      padding: 4rem 2rem;
    }
    .welcome h2 {
      font-size: 2rem;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(5px);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }
    .modal.active { display: flex; }
    .modal-content {
      background: rgba(20, 20, 30, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 1.5rem;
      padding: 2rem;
      max-width: 500px;
      width: 90%;
    }
    .status-bar {
      padding: 0.75rem 2rem;
      background: rgba(20, 20, 30, 0.9);
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      font-size: 0.875rem;
    }
    .status-indicator {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .status-dot {
      width: 0.5rem;
      height: 0.5rem;
      border-radius: 50%;
      background: #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    .thinking-dots {
      display: flex;
      gap: 0.375rem;
    }
    .thinking-dot {
      width: 0.5rem;
      height: 0.5rem;
      border-radius: 50%;
      background: #14b8a6;
      animation: bounce 1s infinite;
    }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-5px); }
    }
    @media (max-width: 768px) {
      .sidebar { display: none; }
      .container { padding: 1rem; }
    }
  </style>
</head>
<body>
  <div class="header glass">
    <div class="logo">Claude Agent</div>
    <div style="display: flex; gap: 0.5rem;">
      <button class="btn btn-glass" onclick="showSettings()">⚙️ Settings</button>
    </div>
  </div>

  <div class="container">
    <div class="sidebar glass">
      <button class="btn btn-primary" onclick="newSession()">+ New Chat</button>
      <div id="sessions"></div>
    </div>

    <div class="chat-panel glass">
      <div class="messages" id="messages">
        <div class="welcome">
          <h2>Welcome to Claude Agent</h2>
          <p style="color: rgba(255,255,255,0.6);">Your glassmorphic AI coding assistant. Set your API key to begin.</p>
        </div>
      </div>
      <div class="input-area">
        <div class="input-container">
          <input type="text" id="input" placeholder="Message Claude..." onkeypress="if(event.key==='Enter') sendMessage()">
          <button class="btn btn-primary" onclick="sendMessage()">Send</button>
        </div>
      </div>
    </div>
  </div>

  <div class="status-bar">
    <div class="status-indicator">
      <div class="status-dot" id="statusDot"></div>
      <span id="statusText">Ready</span>
    </div>
    <div>
      <span style="color: rgba(255,255,255,0.6);">Model: </span>
      <span id="modelName">Claude 3.5 Sonnet</span>
    </div>
  </div>

  <div class="modal" id="settingsModal">
    <div class="modal-content glass">
      <h3 style="margin-bottom: 1rem; color: #14b8a6;">Settings</h3>
      <div style="margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.5rem;">Claude API Key</label>
        <input type="password" id="apiKeyInput" placeholder="sk-ant-..." style="width: 100%;">
      </div>
      <div style="display: flex; gap: 1rem; justify-content: flex-end;">
        <button class="btn btn-glass" onclick="closeSettings()">Cancel</button>
        <button class="btn btn-primary" onclick="saveSettings()">Save</button>
      </div>
    </div>
  </div>

  <script>
    const SUPABASE_URL = 'https://rwybvoxhmnjgunwymujm.supabase.co';
    const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3eWJ2b3hobW5qZ3Vud3ltdWptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgyNDU2MjEsImV4cCI6MjA0MzgyMTYyMX0.67SDuETE3Xw8pVFW_tyLkxBDvQwDyYiSi6Fot6bftvE';
    const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    let apiKey = localStorage.getItem('claude_api_key') || '';
    let currentSessionId = null;
    let messages = [];

    if (!apiKey) showSettings();
    loadSessions();

    async function loadSessions() {
      const { data } = await supabase.from('conversations').select('*').order('updated_at', { ascending: false }).limit(10);
      const list = document.getElementById('sessions');
      list.innerHTML = (data || []).map(s => {
        const active = s.id === currentSessionId ? 'active' : '';
        const titleDiv = '<div style="font-weight: 600; font-size: 0.875rem;">' + s.title + '</div>';
        const dateDiv = '<div style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">' + new Date(s.updated_at).toLocaleDateString() + '</div>';
        return '<div class="session-item ' + active + '" onclick="loadSession(\'' + s.id + '\')">' + titleDiv + dateDiv + '</div>';
      }).join('');
    }

    async function loadSession(id) {
      currentSessionId = id;
      const { data } = await supabase.from('messages').select('*').eq('conversation_id', id).order('created_at');
      messages = data || [];
      renderMessages();
      loadSessions();
    }

    async function newSession() {
      const { data } = await supabase.from('conversations').insert({ title: 'New Chat' }).select().single();
      if (data) {
        currentSessionId = data.id;
        messages = [];
        renderMessages();
        loadSessions();
      }
    }

    function renderMessages() {
      const container = document.getElementById('messages');
      if (messages.length === 0) {
        container.innerHTML = '<div class="welcome"><h2>Start a new conversation</h2><p style="color: rgba(255,255,255,0.6);">Ask Claude anything!</p></div>';
        return;
      }
      container.innerHTML = messages.map(m => {
        const isUser = m.role === 'user';
        const content = parseMarkdown(m.content);
        const avatar = '<div class="avatar">' + (isUser ? '👤' : 'C') + '</div>';
        const bubble = '<div class="bubble">' + content + '</div>';
        return '<div class="message ' + m.role + '">' + avatar + bubble + '</div>';
      }).join('');
      container.scrollTop = container.scrollHeight;
      Prism.highlightAll();
    }

    function parseMarkdown(text) {
      return text.replace(/\`\`\`(\w+)?\n([\s\S]*?)\`\`\`/g, function(match, lang, code) {
        const language = lang || 'javascript';
        const header = '<div class="code-header"><span class="code-lang">' + language + '</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div>';
        const codeBlock = '<pre><code class="language-' + language + '">' + escapeHtml(code.trim()) + '</code></pre>';
        return '<div class="code-block">' + header + codeBlock + '</div>';
      }).replace(/\n/g, '<br>');
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    function copyCode(btn) {
      const code = btn.closest('.code-block').querySelector('code').textContent;
      navigator.clipboard.writeText(code);
      btn.textContent = 'Copied!';
      setTimeout(function() { btn.textContent = 'Copy'; }, 2000);
    }

    async function sendMessage() {
      if (!apiKey) { showSettings(); return; }
      const input = document.getElementById('input');
      const text = input.value.trim();
      if (!text) return;

      if (!currentSessionId) await newSession();

      input.value = '';
      messages.push({ role: 'user', content: text, created_at: new Date().toISOString() });
      await supabase.from('messages').insert({ conversation_id: currentSessionId, role: 'user', content: text });
      renderMessages();

      document.getElementById('statusText').innerHTML = '<div class="thinking-dots"><div class="thinking-dot"></div><div class="thinking-dot"></div><div class="thinking-dot"></div></div>';

      try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01'
          },
          body: JSON.stringify({
            model: 'claude-3-5-sonnet-20241022',
            max_tokens: 4096,
            messages: messages.map(function(m) { return { role: m.role, content: m.content }; })
          })
        });

        const data = await response.json();
        if (data.error) throw new Error(data.error.message);

        const reply = data.content[0].text;
        messages.push({ role: 'assistant', content: reply, created_at: new Date().toISOString() });
        await supabase.from('messages').insert({ conversation_id: currentSessionId, role: 'assistant', content: reply });

        if (messages.length === 2) {
          const title = text.substring(0, 50);
          await supabase.from('conversations').update({ title: title, updated_at: new Date().toISOString() }).eq('id', currentSessionId);
          loadSessions();
        }

        renderMessages();
      } catch (error) {
        messages.push({ role: 'assistant', content: 'Error: ' + error.message, created_at: new Date().toISOString() });
        renderMessages();
      }

      document.getElementById('statusText').textContent = 'Ready';
    }

    function showSettings() {
      document.getElementById('settingsModal').classList.add('active');
      document.getElementById('apiKeyInput').value = apiKey;
    }

    function closeSettings() {
      document.getElementById('settingsModal').classList.remove('active');
    }

    function saveSettings() {
      apiKey = document.getElementById('apiKeyInput').value.trim();
      localStorage.setItem('claude_api_key', apiKey);
      closeSettings();
    }
  </script>
</body>
</html>`;

  return new Response(html, {
    headers: {
      ...corsHeaders,
      "Content-Type": "text/html; charset=utf-8"
    },
  });
});