import { motion, AnimatePresence } from 'framer-motion';
import type { Session } from '../types';

interface SidebarProps {
  isOpen: boolean;
  sessions: Session[];
  currentSessionId?: string | null;
  onSessionSelect: (sessionId: string) => void;
  onNewSession: () => void;
}

export const Sidebar = ({ isOpen, sessions, currentSessionId, onSessionSelect, onNewSession }: SidebarProps) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden"
            onClick={() => {}}
          />
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed left-0 top-0 bottom-0 w-72 glass border-r border-white/10 z-50 flex flex-col"
          >
            <div className="p-4 border-b border-white/10">
              <button
                onClick={onNewSession}
                className="w-full px-4 py-3 rounded-xl bg-teal-500/20 hover:bg-teal-500/30 text-teal-400 font-medium transition-all duration-300 shadow-lg shadow-teal-500/10 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Session
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-2">
              <h3 className="text-white/60 text-xs font-semibold uppercase tracking-wider mb-3">Recent Sessions</h3>
              {sessions.length === 0 ? (
                <div className="text-white/40 text-sm text-center py-8">
                  No sessions yet
                </div>
              ) : (
                sessions.map((session) => (
                  <motion.button
                    key={session.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => onSessionSelect(session.id)}
                    className={`w-full p-3 rounded-lg text-left transition-all duration-200 ${
                      currentSessionId === session.id
                        ? 'bg-teal-500/20 border border-teal-500/30'
                        : 'bg-white/5 hover:bg-white/10 border border-transparent'
                    }`}
                  >
                    <div className="text-white/90 text-sm font-medium truncate">{session.name}</div>
                    <div className="text-white/40 text-xs mt-1">
                      {session.lastMessage ? new Date(session.lastMessage).toLocaleDateString() : 'New'}
                    </div>
                  </motion.button>
                ))
              )}
            </div>

            <div className="p-4 border-t border-white/10">
              <div className="text-white/40 text-xs text-center">
                Connected to ADK Agent
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
};
