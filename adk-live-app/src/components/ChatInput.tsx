import { motion } from 'framer-motion';
import { useState, useRef } from 'react';
import type { KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput = ({ onSend, disabled }: ChatInputProps) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
  };

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass sticky bottom-0 border-t border-white/10 p-4"
    >
      <div className="max-w-4xl mx-auto flex items-end gap-3">
        <button className="p-3 rounded-xl bg-white/5 hover:bg-white/10 text-white/60 transition-all duration-300 flex-shrink-0">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
          </svg>
        </button>

        <div className="flex-1 glass-input rounded-2xl overflow-hidden">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Type a message..."
            className="w-full px-4 py-3 bg-transparent text-white/90 placeholder-white/40 outline-none resize-none"
            style={{ minHeight: '48px', maxHeight: '200px' }}
            rows={1}
          />
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          disabled={!message.trim() || disabled}
          className="p-3 rounded-xl bg-teal-500/20 hover:bg-teal-500/30 text-teal-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg shadow-teal-500/20 flex-shrink-0"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
          </svg>
        </motion.button>
      </div>

      <div className="max-w-4xl mx-auto mt-2 text-center">
        <span className="text-white/40 text-xs">
          Press Enter to send, Shift + Enter for new line
        </span>
      </div>
    </motion.div>
  );
};
