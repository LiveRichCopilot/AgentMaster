import { useState, useEffect, useRef } from 'react';
import { supabase, type Message, type Conversation } from './lib/supabase';
import './App.css';

function App() {
  const [apiKey, setApiKey] = useState(localStorage.getItem('claude_api_key') || '');
  const [showSettings, setShowSettings] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!apiKey) setShowSettings(true);
    loadConversations();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadConversations = async () => {
    const { data } = await supabase
      .from('conversations')
      .select('*')
      .order('updated_at', { ascending: false })
      .limit(10);
    if (data) setConversations(data);
  };

  const loadConversation = async (id: string) => {
    setCurrentConversationId(id);
    const { data } = await supabase
      .from('messages')
      .select('*')
      .eq('conversation_id', id)
      .order('created_at');
    if (data) setMessages(data);
  };

  const createNewConversation = async () => {
    const { data } = await supabase
      .from('conversations')
      .insert({ title: 'New Chat' })
      .select()
      .single();
    if (data) {
      setCurrentConversationId(data.id);
      setMessages([]);
      loadConversations();
    }
  };

  const sendMessage = async () => {
    if (!apiKey) {
      setShowSettings(true);
      return;
    }
    if (!input.trim()) return;

    if (!currentConversationId) await createNewConversation();

    const userMessage = {
      role: 'user' as const,
      content: input,
      conversation_id: currentConversationId!,
    };

    setInput('');
    const newMessages = [...messages, { ...userMessage, id: 'temp', created_at: new Date().toISOString() }];
    setMessages(newMessages);
    setIsThinking(true);

    await supabase.from('messages').insert(userMessage);

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 4096,
          messages: newMessages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });

      const data = await response.json();
      if (data.error) throw new Error(data.error.message);

      const assistantMessage = {
        role: 'assistant' as const,
        content: data.content[0].text,
        conversation_id: currentConversationId!,
      };

      await supabase.from('messages').insert(assistantMessage);

      setMessages([...newMessages, { ...assistantMessage, id: 'temp2', created_at: new Date().toISOString() }]);

      if (newMessages.length === 1) {
        const title = input.substring(0, 50);
        await supabase
          .from('conversations')
          .update({ title, updated_at: new Date().toISOString() })
          .eq('id', currentConversationId);
        loadConversations();
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages([
        ...newMessages,
        {
          id: 'error',
          role: 'assistant',
          content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          conversation_id: currentConversationId!,
          created_at: new Date().toISOString(),
        },
      ]);
    }

    setIsThinking(false);
  };

  const saveApiKey = () => {
    localStorage.setItem('claude_api_key', apiKey);
    setShowSettings(false);
  };

  const parseMarkdown = (text: string) => {
    const parts: React.ReactElement[] = [];
    let lastIndex = 0;
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(<span key={lastIndex} dangerouslySetInnerHTML={{ __html: text.slice(lastIndex, match.index).replace(/\n/g, '<br>') }} />);
      }
      const lang = match[1] || 'text';
      const code = match[2].trim();
      parts.push(
        <div key={match.index} className="code-block">
          <div className="code-header">
            <span className="code-lang">{lang}</span>
          </div>
          <pre><code>{code}</code></pre>
        </div>
      );
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < text.length) {
      parts.push(<span key={lastIndex} dangerouslySetInnerHTML={{ __html: text.slice(lastIndex).replace(/\n/g, '<br>') }} />);
    }

    return <>{parts}</>;
  };

  return (
    <>
      <div className="header glass">
        <div className="logo">Claude Agent</div>
        <button className="btn btn-glass" onClick={() => setShowSettings(true)}>
          ⚙️ Settings
        </button>
      </div>

      <div className="container">
        <div className="sidebar glass">
          <button className="btn btn-primary" onClick={createNewConversation}>
            + New Chat
          </button>
          <div className="sessions">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className={`session-item ${conv.id === currentConversationId ? 'active' : ''}`}
                onClick={() => loadConversation(conv.id)}
              >
                <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>{conv.title}</div>
                <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '0.75rem' }}>
                  {new Date(conv.updated_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="chat-panel glass">
          <div className="messages">
            {messages.length === 0 ? (
              <div className="welcome">
                <h2>Welcome to Claude Agent</h2>
                <p>Your glassmorphic AI coding assistant</p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <div className="avatar">{msg.role === 'user' ? '👤' : 'C'}</div>
                  <div className="bubble">{parseMarkdown(msg.content)}</div>
                </div>
              ))
            )}
            {isThinking && (
              <div className="message assistant">
                <div className="avatar">C</div>
                <div className="bubble">
                  <div className="thinking-dots">
                    <div className="thinking-dot"></div>
                    <div className="thinking-dot"></div>
                    <div className="thinking-dot"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <div className="input-container">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Message Claude..."
              />
              <button className="btn btn-primary" onClick={sendMessage}>
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {showSettings && (
        <div className="modal active" onClick={() => setShowSettings(false)}>
          <div className="modal-content glass" onClick={(e) => e.stopPropagation()}>
            <h3>Settings</h3>
            <div style={{ marginBottom: '1rem' }}>
              <label>Claude API Key</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-ant-..."
                style={{ width: '100%', marginTop: '0.5rem' }}
              />
            </div>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button className="btn btn-glass" onClick={() => setShowSettings(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={saveApiKey}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
