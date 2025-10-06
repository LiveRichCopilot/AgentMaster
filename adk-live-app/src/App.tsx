import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { VoiceControl } from './components/VoiceControl';
import { CodeEditor } from './components/CodeEditor';
import { Settings } from './components/Settings';
import { StatusBar } from './components/StatusBar';
import type { Message, AgentStatus, Session } from './types';
import { useAgentStore } from './store/useAgentStore';
import { claudeService } from './services/claudeService';
import { supabaseService } from './services/supabaseService';
import { voiceService } from './services/voiceService';

function App() {
  const {
    messages,
    sessions,
    currentSessionId,
    isThinking,
    isStreaming,
    apiKey,
    settings,
    setMessages,
    addMessage,
    setSessions,
    setCurrentSessionId,
    setIsThinking,
    setIsStreaming,
    setTokenUsage,
    clearMessages,
  } = useAgentStore();

  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    online: !!apiKey,
    thinking: false,
    responding: false,
  });
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showCodeEditor, setShowCodeEditor] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [code, setCode] = useState('# Write your Python code here\nprint("Hello from Claude Agent!")');
  const [codeLanguage] = useState('python');
  const [codeOutput, setCodeOutput] = useState<string>();
  const [codeError, setCodeError] = useState<string>();
  const [isRunningCode, setIsRunningCode] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const transcriptTimeoutRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  // Initialize services
  useEffect(() => {
    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
    const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

    if (supabaseUrl && supabaseKey) {
      supabaseService.initialize(supabaseUrl, supabaseKey);
    }

    if (apiKey) {
      claudeService.initialize(apiKey);
      setAgentStatus((prev) => ({ ...prev, online: true }));
    } else {
      setShowSettings(true);
    }

    loadSessions();
  }, [apiKey]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadSessions = async () => {
    try {
      const sessionsData = await supabaseService.getSessions();
      const formattedSessions: Session[] = sessionsData.map(s => ({
        id: s.id,
        name: s.title,
        createdAt: new Date(s.created_at),
        lastMessage: new Date(s.updated_at),
      }));
      setSessions(formattedSessions);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!apiKey) {
      setShowSettings(true);
      return;
    }

    // Create or ensure session exists
    let sessionId = currentSessionId;
    if (!sessionId) {
      const newSession = await supabaseService.createSession('New Conversation');
      if (newSession) {
        sessionId = newSession.id;
        setCurrentSessionId(sessionId);
        await loadSessions();
      }
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setIsThinking(true);
    setAgentStatus((prev) => ({ ...prev, thinking: true }));

    // Save user message
    if (sessionId) {
      await supabaseService.saveMessage(sessionId, 'user', content);
    }

    try {
      // Convert messages to Claude format
      const claudeMessages = [...messages, userMessage].map(m => ({
        role: m.role,
        content: m.content,
      }));

      let fullResponse = '';
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      };

      setIsStreaming(true);

      // Stream the response
      for await (const chunk of claudeService.streamMessage(
        claudeMessages,
        settings.model,
        settings.maxTokens,
        settings.temperature
      )) {
        fullResponse = chunk.text;
        assistantMessage.content = fullResponse;

        // Update the message in place
        setMessages([...messages, userMessage, { ...assistantMessage }]);

        if (chunk.done) {
          setIsStreaming(false);
          setIsThinking(false);
          setAgentStatus((prev) => ({ ...prev, thinking: false, responding: false }));

          // Save assistant message
          if (sessionId) {
            await supabaseService.saveMessage(sessionId, 'assistant', fullResponse);

            // Update session title with first user message if needed
            if (messages.length === 0) {
              const title = content.substring(0, 50) + (content.length > 50 ? '...' : '');
              await supabaseService.updateSessionTitle(sessionId, title);
              await loadSessions();
            }
          }

          // Speak response if voice enabled
          if (voiceEnabled) {
            voiceService.speak(fullResponse);
          }

          // Estimate token usage (rough estimate)
          const estimatedTokens = Math.ceil((content.length + fullResponse.length) / 4);
          setTokenUsage(estimatedTokens);
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please check your API key and try again.',
        timestamp: new Date(),
      };
      addMessage(errorMessage);
      setIsThinking(false);
      setIsStreaming(false);
      setAgentStatus((prev) => ({ ...prev, thinking: false }));
    }
  };

  const handleStartListening = () => {
    if (!voiceService.isRecognitionAvailable()) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    setIsListening(true);
    voiceService.startListening(
      (text, isFinal) => {
        setTranscript(text);

        if (transcriptTimeoutRef.current) {
          clearTimeout(transcriptTimeoutRef.current);
        }

        if (isFinal) {
          transcriptTimeoutRef.current = setTimeout(() => {
            if (text.trim()) {
              handleSendMessage(text);
              setTranscript('');
              setIsListening(false);
            }
          }, 2000);
        }
      },
      () => {
        setIsListening(false);
      },
      (error) => {
        console.error('Speech recognition error:', error);
        setIsListening(false);
      }
    );
  };

  const handleStopListening = () => {
    voiceService.stopListening();
    setIsListening(false);

    if (transcript.trim()) {
      handleSendMessage(transcript);
    }
    setTranscript('');
  };

  const handleRunCode = async () => {
    setIsRunningCode(true);
    setCodeOutput(undefined);
    setCodeError(undefined);

    // For now, just simulate code execution
    // In a real implementation, you'd call a backend service
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCodeOutput('Code execution feature coming soon!\nThis will integrate with a Python/JS runtime.');
    } catch (error) {
      setCodeError(error instanceof Error ? error.message : 'Failed to execute code');
    } finally {
      setIsRunningCode(false);
    }
  };

  const handleNewSession = async () => {
    const newSession = await supabaseService.createSession('New Conversation');
    if (newSession) {
      setCurrentSessionId(newSession.id);
      clearMessages();
      await loadSessions();
      setSidebarOpen(false);
    }
  };

  const handleSessionSelect = async (sessionId: string) => {
    setCurrentSessionId(sessionId);

    // Load messages for this session
    const messagesData = await supabaseService.getMessages(sessionId);
    const formattedMessages: Message[] = messagesData.map(m => ({
      id: m.id,
      role: m.role,
      content: m.content,
      timestamp: new Date(m.created_at),
    }));

    setMessages(formattedMessages);
    setSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex flex-col">
      <Header
        agentStatus={agentStatus}
        voiceEnabled={voiceEnabled}
        onVoiceToggle={() => setVoiceEnabled(!voiceEnabled)}
        onSettingsClick={() => setShowSettings(true)}
      />

      <Sidebar
        isOpen={sidebarOpen}
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSessionSelect={handleSessionSelect}
        onNewSession={handleNewSession}
      />

      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-4xl mx-auto">
            <AnimatePresence mode="popLayout">
              {messages.length === 0 ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="text-center py-20"
                >
                  <div className="w-24 h-24 mx-auto mb-8 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-2xl shadow-teal-500/40">
                    <span className="text-white font-bold text-3xl">C</span>
                  </div>
                  <h2 className="text-3xl font-bold text-white mb-4">
                    Welcome to Claude Agent
                  </h2>
                  <p className="text-white/60 mb-12 text-lg">
                    Your intelligent coding companion with glassmorphic style
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto mb-8">
                    <motion.button
                      whileHover={{ scale: 1.02, y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleSendMessage('Help me write a Python function')}
                      className="glass rounded-2xl p-8 text-left hover:bg-white/15 transition-all duration-300 group"
                    >
                      <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">💻</div>
                      <div className="text-white font-semibold mb-2 text-lg">Code with Claude</div>
                      <div className="text-white/60">Get help writing and debugging code</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02, y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setShowCodeEditor(!showCodeEditor)}
                      className="glass rounded-2xl p-8 text-left hover:bg-white/15 transition-all duration-300 group"
                    >
                      <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">⚡</div>
                      <div className="text-white font-semibold mb-2 text-lg">Live Editor</div>
                      <div className="text-white/60">Write and run code in real-time</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02, y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setSidebarOpen(true)}
                      className="glass rounded-2xl p-8 text-left hover:bg-white/15 transition-all duration-300 group"
                    >
                      <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">📚</div>
                      <div className="text-white font-semibold mb-2 text-lg">Sessions</div>
                      <div className="text-white/60">View and manage your chat history</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02, y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleStartListening}
                      className="glass rounded-2xl p-8 text-left hover:bg-white/15 transition-all duration-300 group"
                    >
                      <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🎤</div>
                      <div className="text-white font-semibold mb-2 text-lg">Voice Chat</div>
                      <div className="text-white/60">Talk to Claude with your voice</div>
                    </motion.button>
                  </div>

                  {voiceEnabled && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex justify-center"
                    >
                      <VoiceControl
                        isListening={isListening}
                        transcript={transcript}
                        onStartListening={handleStartListening}
                        onStopListening={handleStopListening}
                      />
                    </motion.div>
                  )}
                </motion.div>
              ) : (
                <>
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                  {isThinking && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex items-center gap-3 mb-6"
                    >
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/40">
                        <span className="font-bold text-sm text-white">C</span>
                      </div>
                      <div className="glass rounded-2xl px-6 py-4 bg-white/10">
                        <div className="flex gap-1.5">
                          <motion.div
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                            className="w-2.5 h-2.5 rounded-full bg-teal-400"
                          />
                          <motion.div
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                            className="w-2.5 h-2.5 rounded-full bg-teal-400"
                          />
                          <motion.div
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                            className="w-2.5 h-2.5 rounded-full bg-teal-400"
                          />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </>
              )}
            </AnimatePresence>

            {showCodeEditor && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-8"
              >
                <CodeEditor
                  code={code}
                  language={codeLanguage}
                  onChange={setCode}
                  onRun={handleRunCode}
                  output={codeOutput}
                  error={codeError}
                  isRunning={isRunningCode}
                />
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        <ChatInput onSend={handleSendMessage} disabled={isThinking || isStreaming} />
      </main>

      <StatusBar />

      <Settings isOpen={showSettings} onClose={() => setShowSettings(false)} />

      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="fixed left-4 top-20 z-40 p-3 rounded-xl glass hover:bg-white/15 transition-all duration-300 md:hidden"
      >
        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {voiceEnabled && messages.length > 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="fixed bottom-28 right-6 z-30"
        >
          <VoiceControl
            isListening={isListening}
            transcript={transcript}
            onStartListening={handleStartListening}
            onStopListening={handleStopListening}
          />
        </motion.div>
      )}
    </div>
  );
}

export default App;
