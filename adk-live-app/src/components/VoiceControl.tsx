import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

interface VoiceControlProps {
  isListening: boolean;
  transcript: string;
  onStartListening: () => void;
  onStopListening: () => void;
}

export const VoiceControl = ({ isListening, transcript, onStartListening, onStopListening }: VoiceControlProps) => {
  const [, setAudioLevel] = useState(0);

  useEffect(() => {
    if (isListening) {
      const interval = setInterval(() => {
        setAudioLevel(Math.random() * 100);
      }, 100);
      return () => clearInterval(interval);
    } else {
      setAudioLevel(0);
    }
  }, [isListening]);

  return (
    <div className="flex items-center gap-4">
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={isListening ? onStopListening : onStartListening}
        className={`relative w-14 h-14 rounded-full flex items-center justify-center transition-all duration-300 ${
          isListening
            ? 'bg-red-500/20 text-red-400 shadow-2xl shadow-red-500/40'
            : 'bg-teal-500/20 text-teal-400 hover:bg-teal-500/30 shadow-lg shadow-teal-500/20'
        }`}
      >
        {isListening && (
          <motion.div
            initial={{ scale: 1, opacity: 0.8 }}
            animate={{ scale: 1.5, opacity: 0 }}
            transition={{ repeat: Infinity, duration: 1.5 }}
            className="absolute inset-0 rounded-full bg-red-500/30"
          />
        )}

        <svg className="w-6 h-6 relative z-10" fill="currentColor" viewBox="0 0 20 20">
          {isListening ? (
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" />
          ) : (
            <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
          )}
        </svg>
      </motion.button>

      <AnimatePresence>
        {isListening && (
          <motion.div
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: 'auto' }}
            exit={{ opacity: 0, width: 0 }}
            className="flex items-center gap-3"
          >
            <div className="flex gap-1 items-end h-8">
              {[...Array(20)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={{
                    height: isListening ? `${(Math.sin(Date.now() / 100 + i) + 1) * 50}%` : '10%'
                  }}
                  transition={{ duration: 0.1 }}
                  className="w-1 bg-gradient-to-t from-teal-600 to-teal-400 rounded-full"
                  style={{ minHeight: '4px' }}
                />
              ))}
            </div>

            {transcript && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="glass-input px-4 py-2 rounded-lg text-white/90 text-sm max-w-xs"
              >
                {transcript}
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
