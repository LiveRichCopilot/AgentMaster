import { motion } from 'framer-motion';
import type { AgentStatus } from '../types';

interface HeaderProps {
  agentStatus: AgentStatus;
  voiceEnabled: boolean;
  onVoiceToggle: () => void;
  onSettingsClick: () => void;
}

export const Header = ({ agentStatus, voiceEnabled, onVoiceToggle, onSettingsClick }: HeaderProps) => {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass sticky top-0 z-50 px-4 py-3 border-b border-white/10"
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-lg shadow-teal-500/30">
            <span className="text-white font-bold text-sm">LIV</span>
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">LIV Assistant</h1>
            <div className="flex items-center gap-2 text-xs">
              <div className={`w-2 h-2 rounded-full ${agentStatus.online ? 'bg-green-400' : 'bg-red-400'} ${agentStatus.online ? 'pulse-glow' : ''}`}></div>
              <span className="text-white/60">
                {agentStatus.thinking ? 'Thinking...' : agentStatus.responding ? 'Responding...' : agentStatus.online ? 'Ready' : 'Offline'}
              </span>
              {agentStatus.currentTool && (
                <span className="text-teal-400">• {agentStatus.currentTool}</span>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onVoiceToggle}
            className={`p-2 rounded-xl transition-all duration-300 ${
              voiceEnabled
                ? 'bg-teal-500/20 text-teal-400 shadow-lg shadow-teal-500/20'
                : 'bg-white/5 text-white/40 hover:bg-white/10'
            }`}
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              {voiceEnabled ? (
                <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
              ) : (
                <path fillRule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clipRule="evenodd" />
              )}
            </svg>
          </button>

          <button
            onClick={onSettingsClick}
            className="p-2 rounded-xl bg-white/5 text-white/60 hover:bg-white/10 hover:text-white transition-all duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </div>
    </motion.header>
  );
};
