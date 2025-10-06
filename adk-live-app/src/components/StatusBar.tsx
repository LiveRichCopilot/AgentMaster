import { motion } from 'framer-motion';
import { useAgentStore } from '../store/useAgentStore';

export function StatusBar() {
  const { isThinking, isStreaming, settings, tokenUsage, apiKey } = useAgentStore();

  const getStatusText = () => {
    if (isStreaming) return 'Streaming response...';
    if (isThinking) return 'Thinking...';
    return 'Ready';
  };

  const getStatusColor = () => {
    if (isStreaming || isThinking) return 'text-teal-400';
    return 'text-green-400';
  };

  return (
    <div className="glass border-t border-white/10">
      <div className="px-6 py-3 flex items-center justify-between text-sm">
        <div className="flex items-center gap-6">
          {/* Connection Status */}
          <div className="flex items-center gap-2">
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className={`w-2 h-2 rounded-full ${apiKey ? 'bg-green-400' : 'bg-red-400'}`}
            />
            <span className={`font-medium ${getStatusColor()}`}>
              {getStatusText()}
            </span>
          </div>

          {/* Model Info */}
          <div className="text-white/60">
            <span className="hidden sm:inline">Model: </span>
            <span className="text-white">{settings.model.split('-')[2]}</span>
          </div>

          {/* Temperature */}
          <div className="text-white/60 hidden md:block">
            <span>Temp: </span>
            <span className="text-white">{settings.temperature.toFixed(1)}</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Token Usage */}
          <div className="text-white/60 hidden sm:block">
            <span>Tokens: </span>
            <span className="text-white">{tokenUsage.toLocaleString()}</span>
          </div>

          {/* API Status */}
          <div className="flex items-center gap-2">
            {apiKey ? (
              <span className="text-green-400 text-xs px-2 py-1 rounded-lg bg-green-400/10 border border-green-400/20">
                API Connected
              </span>
            ) : (
              <span className="text-red-400 text-xs px-2 py-1 rounded-lg bg-red-400/10 border border-red-400/20">
                API Key Required
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
