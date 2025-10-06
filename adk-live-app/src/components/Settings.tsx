import { motion, AnimatePresence } from 'framer-motion';
import { useAgentStore } from '../store/useAgentStore';
import { claudeService } from '../services/claudeService';

interface SettingsProps {
  isOpen: boolean;
  onClose: () => void;
}

export function Settings({ isOpen, onClose }: SettingsProps) {
  const { settings, apiKey, setApiKey, updateSettings } = useAgentStore();

  const handleApiKeySubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const key = formData.get('apiKey') as string;
    if (key) {
      setApiKey(key);
      claudeService.initialize(key);
    }
  };

  const models = [
    { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet (Recommended)' },
    { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus (Most Capable)' },
    { value: 'claude-3-sonnet-20240229', label: 'Claude 3 Sonnet' },
    { value: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku (Fastest)' },
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
          >
            <div className="glass rounded-3xl p-8 m-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Settings</h2>
                <button
                  onClick={onClose}
                  className="glass rounded-xl p-2 hover:bg-white/15 transition-all"
                >
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* API Key Section */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-teal-400">🔑</span>
                  Claude API Key
                </h3>
                <form onSubmit={handleApiKeySubmit} className="space-y-4">
                  <div>
                    <input
                      type="password"
                      name="apiKey"
                      defaultValue={apiKey || ''}
                      placeholder="sk-ant-..."
                      className="glass-input w-full px-4 py-3 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-teal-500/50"
                    />
                    <p className="text-white/60 text-sm mt-2">
                      Get your API key from{' '}
                      <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer" className="text-teal-400 hover:text-teal-300">
                        console.anthropic.com
                      </a>
                    </p>
                  </div>
                  <button
                    type="submit"
                    className="glass rounded-xl px-6 py-3 bg-teal-500/20 border-teal-500/30 hover:bg-teal-500/30 text-white font-medium transition-all"
                  >
                    Save API Key
                  </button>
                </form>
              </div>

              {/* Model Selection */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-teal-400">🤖</span>
                  Model
                </h3>
                <select
                  value={settings.model}
                  onChange={(e) => updateSettings({ model: e.target.value })}
                  className="glass-input w-full px-4 py-3 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-teal-500/50"
                >
                  {models.map((model) => (
                    <option key={model.value} value={model.value} className="bg-black">
                      {model.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Temperature */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-teal-400">🌡️</span>
                  Temperature: {settings.temperature.toFixed(1)}
                </h3>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.temperature}
                  onChange={(e) => updateSettings({ temperature: parseFloat(e.target.value) })}
                  className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-teal-500"
                />
                <div className="flex justify-between text-white/60 text-sm mt-2">
                  <span>Precise</span>
                  <span>Creative</span>
                </div>
              </div>

              {/* Max Tokens */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-teal-400">📊</span>
                  Max Tokens
                </h3>
                <input
                  type="number"
                  value={settings.maxTokens}
                  onChange={(e) => updateSettings({ maxTokens: parseInt(e.target.value) })}
                  min="100"
                  max="8192"
                  step="100"
                  className="glass-input w-full px-4 py-3 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-teal-500/50"
                />
                <p className="text-white/60 text-sm mt-2">
                  Maximum tokens in the response (100-8192)
                </p>
              </div>

              {/* System Prompt */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-teal-400">💬</span>
                  System Prompt
                </h3>
                <textarea
                  value={settings.systemPrompt}
                  onChange={(e) => updateSettings({ systemPrompt: e.target.value })}
                  rows={4}
                  className="glass-input w-full px-4 py-3 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-teal-500/50 resize-none"
                  placeholder="Set the agent's behavior and personality..."
                />
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
