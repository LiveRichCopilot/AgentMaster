"use client";

import { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';
import { AgentSidebar, AgentStatus } from '@/components/AgentSidebar';
import { StatusBar, StatusUpdate } from '@/components/StatusBar';
import { TracePanel, TraceEvent } from '@/components/TracePanel';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  agent?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hello! I'm JAi Cortex - your 24-agent development team. I have specialists for every aspect of software development. What would you like to build today?",
      timestamp: Date.now(),
      agent: 'Project Manager'
    }
  ]);
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatus>>({});
  const [currentStatus, setCurrentStatus] = useState<StatusUpdate>();
  const [traceEvents, setTraceEvents] = useState<TraceEvent[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const startTime = Date.now(); // Start timer

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = input;
    setInput('');
    setIsLoading(true);

    // Add loading indicator message
    const loadingId = 'loading-' + Date.now();
    setMessages(prev => [...prev, {
      id: loadingId,
      role: 'assistant',
      content: '⏳ JAi Cortex is thinking...',
      timestamp: Date.now()
    }]);

    // Add trace for user message
    setTraceEvents(prev => [...prev, {
      id: `user-msg-${Date.now()}-${Math.random()}`,
      timestamp: Date.now(),
      type: 'message',
      fromAgent: 'User',
      action: 'Message sent',
      details: messageToSend.substring(0, 100)
    }]);

    try {
      // Use local JAi Cortex OS backend with complete ADK system
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageToSend,
          session_id: 'main-session',  // Fixed session ID for conversation continuity
          user_id: 'default'
        })
      });

      const data = await response.json();
      const responseTime = ((Date.now() - startTime) / 1000).toFixed(2); // Calculate response time in seconds
      
      // Add tool calls to trace (if any)
      if (data.tool_calls && data.tool_calls.length > 0) {
        data.tool_calls.forEach((toolCall: { name: string; args: Record<string, unknown> }) => {
          setTraceEvents(prev => [...prev, {
            id: `tool-${Date.now()}-${Math.random()}`,
            timestamp: Date.now(),
            type: 'tool_use',
            fromAgent: 'JAi Cortex',
            action: `Tool: ${toolCall.name}`,
            details: JSON.stringify(toolCall.args, null, 2)
          }]);
        });
      }
      
      // ALWAYS add response trace with timing
      setTraceEvents(prev => [...prev, {
        id: `response-${Date.now()}-${Math.random()}`,
        timestamp: Date.now(),
        type: 'response',
        fromAgent: 'JAi Cortex',
        action: `Response generated in ${responseTime}s`,
        details: data.response.substring(0, 150) + (data.response.length > 150 ? '...' : '')
      }]);
      
      // Remove loading message and add real response
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== loadingId);
        return [...filtered, {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          timestamp: Date.now()
        }];
      });

      setIsLoading(false);
    } catch (error) {
      console.error('Error:', error);
      const errorTime = ((Date.now() - startTime) / 1000).toFixed(2);
      
      // Remove loading message and show error
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== loadingId);
        return [...filtered, {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: '❌ Sorry, I encountered an error. Please try again.',
          timestamp: Date.now()
        }];
      });
      
      // Add error trace with timing
      setTraceEvents(prev => [...prev, {
        id: `trace-error-${Date.now()}-${Math.random()}`,
        timestamp: Date.now(),
        type: 'error',
        fromAgent: 'System',
        action: `Request failed after ${errorTime}s`,
        details: error instanceof Error ? error.message : 'Unknown error'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // Voice recording logic would go here
  };

  return (
    <div className="flex h-screen w-full bg-neutral-950 relative overflow-hidden">
      {/* Animated blurred orbs in background */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Teal orb */}
        <div className="absolute w-96 h-96 bg-teal-500/20 rounded-full blur-3xl animate-float-slow top-0 -left-20" />
        <div className="absolute w-80 h-80 bg-teal-400/15 rounded-full blur-3xl animate-float-medium bottom-20 right-10" />
        
        {/* Blue orbs */}
        <div className="absolute w-72 h-72 bg-sky-400/20 rounded-full blur-3xl animate-float-medium top-40 right-0" />
        <div className="absolute w-64 h-64 bg-blue-500/15 rounded-full blur-3xl animate-float-slow bottom-0 left-1/3" />
        
        {/* Pink orbs */}
        <div className="absolute w-60 h-60 bg-pink-400/10 rounded-full blur-3xl animate-float-fast top-1/3 left-1/4" />
        <div className="absolute w-56 h-56 bg-pink-500/15 rounded-full blur-3xl animate-float-medium bottom-40 right-1/4" />
      </div>
      
      {/* Agent Sidebar */}
      <AgentSidebar agentStatuses={agentStatuses} />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Status Bar */}
        <StatusBar currentStatus={currentStatus} />

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xl rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-teal-500/20 border border-teal-400/40'
                    : 'bg-neutral-800/50 border border-neutral-700/50'
                }`}
              >
                {message.agent && (
                  <div className="text-xs font-medium text-cyan-400 mb-2">
                    {message.agent}
                  </div>
                )}
                <p className="text-gray-100 whitespace-pre-wrap">{message.content}</p>
                <div className="text-xs text-gray-500 mt-2" suppressHydrationWarning>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-neutral-800/50 bg-neutral-900/80 backdrop-blur-xl p-4">
          <div className="flex items-end gap-3">
            <button
              onClick={toggleRecording}
              className={`p-3 rounded-xl transition-all ${
                isRecording
                  ? 'bg-red-500 hover:bg-red-600'
                  : 'bg-neutral-800 hover:bg-neutral-700'
              }`}
            >
              {isRecording ? (
                <MicOff className="w-5 h-5 text-white" />
              ) : (
                <Mic className="w-5 h-5 text-white" />
              )}
            </button>

            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Describe what you want to build..."
                className="w-full bg-neutral-900/50 border border-neutral-800/50 rounded-xl px-4 py-3 text-gray-100 placeholder-neutral-500 focus:outline-none focus:border-cyan-400/50 resize-none"
                rows={1}
                style={{ minHeight: '48px', maxHeight: '120px' }}
              />
            </div>

            <button
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
              className="p-3 bg-sky-400 hover:bg-sky-500 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-sky-500/20"
            >
              <Send className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </div>

      {/* Trace Panel */}
      <TracePanel events={traceEvents} />
      
      {/* Floating orb animations */}
      <style jsx>{`
        @keyframes float-slow {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(30px, -40px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 40px) scale(0.9);
          }
        }
        
        @keyframes float-medium {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          50% {
            transform: translate(-40px, -50px) scale(1.15);
          }
        }
        
        @keyframes float-fast {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          25% {
            transform: translate(50px, 30px) scale(0.95);
          }
          75% {
            transform: translate(-30px, -40px) scale(1.05);
          }
        }
        
        .animate-float-slow {
          animation: float-slow 20s ease-in-out infinite;
        }
        
        .animate-float-medium {
          animation: float-medium 15s ease-in-out infinite;
        }
        
        .animate-float-fast {
          animation: float-fast 12s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
