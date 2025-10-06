import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { VoiceControl } from './components/VoiceControl';
import { CodeEditor } from './components/CodeEditor';
import type { Message, AgentStatus, Session } from './types';
import { adkService } from './services/adkService';
import { voiceService } from './services/voiceService';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    online: false,
    thinking: false,
    responding: false,
  });
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string>();
  const [showCodeEditor, setShowCodeEditor] = useState(false);
  const [code, setCode] = useState('# Write your Python code here\nprint("Hello from LIV!")');
  const [codeLanguage] = useState('python');
  const [codeOutput, setCodeOutput] = useState<string>();
  const [codeError, setCodeError] = useState<string>();
  const [isRunningCode, setIsRunningCode] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const transcriptTimeoutRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    adkService.connect();

    const unsubscribeMessage = adkService.onMessage((message) => {
      setMessages((prev) => [...prev, message]);
      setAgentStatus((prev) => ({ ...prev, thinking: false, responding: false }));

      if (voiceEnabled && message.role === 'assistant') {
        voiceService.speak(message.content);
      }
    });

    const unsubscribeStatus = adkService.onStatus((status) => {
      setAgentStatus((prev) => ({ ...prev, ...status }));
    });

    loadSessions();

    return () => {
      unsubscribeMessage();
      unsubscribeStatus();
      adkService.disconnect();
    };
  }, [voiceEnabled]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadSessions = async () => {
    try {
      const sessionsData = await adkService.getSessions();
      setSessions(sessionsData);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setAgentStatus((prev) => ({ ...prev, thinking: true }));

    try {
      await adkService.sendMessage(content);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the ADK agent is running on http://127.0.0.1:8000',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
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

    try {
      const result = await adkService.executeCode(code, codeLanguage);

      if (result.error) {
        setCodeError(result.error);
      } else {
        setCodeOutput(result.output || 'Code executed successfully (no output)');
      }
    } catch (error) {
      setCodeError(error instanceof Error ? error.message : 'Failed to execute code');
    } finally {
      setIsRunningCode(false);
    }
  };

  const handleNewSession = () => {
    const newSession: Session = {
      id: Date.now().toString(),
      name: `Session ${sessions.length + 1}`,
      createdAt: new Date(),
    };
    setSessions((prev) => [newSession, ...prev]);
    setCurrentSessionId(newSession.id);
    setMessages([]);
    setSidebarOpen(false);
  };

  const handleSessionSelect = (sessionId: string) => {
    setCurrentSessionId(sessionId);
    setSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex flex-col">
      <Header
        agentStatus={agentStatus}
        voiceEnabled={voiceEnabled}
        onVoiceToggle={() => setVoiceEnabled(!voiceEnabled)}
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
                  <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-2xl shadow-teal-500/40">
                    <span className="text-white font-bold text-2xl">LIV</span>
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-3">
                    Welcome to LIV Assistant
                  </h2>
                  <p className="text-white/60 mb-8">
                    Your intelligent coding companion powered by ADK
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto mb-8">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleSendMessage('Help me write a Python function')}
                      className="glass rounded-xl p-6 text-left hover:bg-white/15 transition-all duration-300"
                    >
                      <div className="text-teal-400 mb-2">💻</div>
                      <div className="text-white font-medium mb-1">Code with me</div>
                      <div className="text-white/60 text-sm">Get help writing and debugging code</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setShowCodeEditor(!showCodeEditor)}
                      className="glass rounded-xl p-6 text-left hover:bg-white/15 transition-all duration-300"
                    >
                      <div className="text-teal-400 mb-2">⚡</div>
                      <div className="text-white font-medium mb-1">Live Editor</div>
                      <div className="text-white/60 text-sm">Write and run code in real-time</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setSidebarOpen(true)}
                      className="glass rounded-xl p-6 text-left hover:bg-white/15 transition-all duration-300"
                    >
                      <div className="text-teal-400 mb-2">📚</div>
                      <div className="text-white font-medium mb-1">Sessions</div>
                      <div className="text-white/60 text-sm">View and manage your chat history</div>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleStartListening}
                      className="glass rounded-xl p-6 text-left hover:bg-white/15 transition-all duration-300"
                    >
                      <div className="text-teal-400 mb-2">🎤</div>
                      <div className="text-white font-medium mb-1">Voice Chat</div>
                      <div className="text-white/60 text-sm">Talk to LIV with your voice</div>
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
                  {agentStatus.thinking && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex items-center gap-3 mb-4"
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/30">
                        <span className="font-bold text-xs text-white">L</span>
                      </div>
                      <div className="glass rounded-2xl px-6 py-4 bg-white/10">
                        <div className="flex gap-1">
                          <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                            className="w-2 h-2 rounded-full bg-teal-400"
                          />
                          <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                            className="w-2 h-2 rounded-full bg-teal-400"
                          />
                          <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                            className="w-2 h-2 rounded-full bg-teal-400"
                          />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </>
              )}
            </AnimatePresence>

            {showCodeEditor && (
              <div className="mt-8">
                <CodeEditor
                  code={code}
                  language={codeLanguage}
                  onChange={setCode}
                  onRun={handleRunCode}
                  output={codeOutput}
                  error={codeError}
                  isRunning={isRunningCode}
                />
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        <ChatInput onSend={handleSendMessage} disabled={agentStatus.thinking} />
      </main>

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
          className="fixed bottom-24 right-6 z-30"
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
