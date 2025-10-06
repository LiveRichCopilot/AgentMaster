import { motion } from 'framer-motion';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
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

  type ContentPart = { type: 'text'; content: string } | { type: 'code'; content: string; language: string };

  const parseContent = (): ContentPart[] => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts: ContentPart[] = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(message.content)) !== null) {
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: message.content.slice(lastIndex, match.index),
        });
      }

      parts.push({
        type: 'code',
        content: match[2].trim(),
        language: match[1] || 'text',
      });

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < message.content.length) {
      parts.push({
        type: 'text',
        content: message.content.slice(lastIndex),
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content: message.content }];
  };

  const renderContent = () => {
    const parts = parseContent();

    return (
      <div className="space-y-3">
        {parts.map((part, index) => {
          if (part.type === 'code') {
            return (
              <div key={index} className="relative group">
                <div className="flex items-center justify-between mb-2 px-4 py-2 bg-black/40 rounded-t-xl">
                  <span className="text-teal-400 text-xs font-mono font-semibold uppercase">
                    {part.language}
                  </span>
                  <button
                    onClick={() => handleCopy(part.content)}
                    className="text-white/60 hover:text-white transition-colors text-xs flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-white/10"
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
                <div className="rounded-b-xl overflow-hidden">
                  <SyntaxHighlighter
                    language={part.language}
                    style={vscDarkPlus}
                    customStyle={{
                      margin: 0,
                      padding: '1rem',
                      background: 'rgba(0, 0, 0, 0.4)',
                      fontSize: '0.875rem',
                    }}
                    showLineNumbers
                  >
                    {part.content}
                  </SyntaxHighlighter>
                </div>
              </div>
            );
          }

          return (
            <div key={index} className="text-white/90 whitespace-pre-wrap break-words leading-relaxed">
              {part.content}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}
    >
      <div className={`flex gap-3 max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser
            ? 'glass bg-white/5 text-white/90'
            : 'bg-gradient-to-br from-teal-500 to-teal-600 text-white shadow-lg shadow-teal-500/40'
        }`}>
          {isUser ? (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          ) : (
            <span className="font-bold text-sm">L</span>
          )}
        </div>

        <div className={`glass rounded-2xl p-5 ${
          isUser
            ? 'bg-gradient-to-br from-teal-500/20 to-teal-600/10 border-teal-500/30'
            : 'bg-white/5'
        }`}>
          {renderContent()}

          {message.toolUsed && (
            <div className="mt-3 pt-3 border-t border-white/10">
              <span className="text-teal-400 text-xs font-medium flex items-center gap-1">
                <span>🛠️</span> {message.toolUsed}
              </span>
            </div>
          )}

          <div className="mt-3 text-white/40 text-xs">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
