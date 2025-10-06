import { motion } from 'framer-motion';
import type { Message } from '../types';
import { useState } from 'react';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderContent = () => {
    if (message.isCode && message.codeLanguage) {
      return (
        <div className="relative group">
          <div className="flex items-center justify-between mb-2 px-3 py-1 bg-black/30 rounded-t-lg">
            <span className="text-teal-400 text-xs font-mono">{message.codeLanguage}</span>
            <button
              onClick={() => handleCopy(message.content)}
              className="text-white/60 hover:text-white transition-colors text-xs flex items-center gap-1"
            >
              {copied ? (
                <>
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Copied
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Copy
                </>
              )}
            </button>
          </div>
          <pre className="bg-black/30 p-3 rounded-b-lg overflow-x-auto">
            <code className="text-sm font-mono text-white/90">{message.content}</code>
          </pre>
        </div>
      );
    }

    return (
      <div className="text-white/90 whitespace-pre-wrap break-words">
        {message.content}
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`flex gap-3 max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser
            ? 'bg-white/10 text-white/90'
            : 'bg-gradient-to-br from-teal-500 to-teal-600 text-white shadow-lg shadow-teal-500/30'
        }`}>
          {isUser ? (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          ) : (
            <span className="font-bold text-xs">L</span>
          )}
        </div>

        <div className={`glass rounded-2xl p-4 ${
          isUser ? 'bg-white/5' : 'bg-white/10'
        }`}>
          {renderContent()}

          {message.toolUsed && (
            <div className="mt-2 pt-2 border-t border-white/10">
              <span className="text-teal-400 text-xs">🛠️ {message.toolUsed}</span>
            </div>
          )}

          <div className="mt-2 text-white/40 text-xs">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
