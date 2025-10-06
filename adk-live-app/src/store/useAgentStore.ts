import { create } from 'zustand';
import type { Message, Session } from '../types';

export interface AgentSettings {
  model: string;
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
}

interface AgentStore {
  messages: Message[];
  sessions: Session[];
  currentSessionId: string | null;
  isThinking: boolean;
  isStreaming: boolean;
  apiKey: string | null;
  settings: AgentSettings;
  tokenUsage: number;

  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  setSessions: (sessions: Session[]) => void;
  setCurrentSessionId: (id: string | null) => void;
  setIsThinking: (thinking: boolean) => void;
  setIsStreaming: (streaming: boolean) => void;
  setApiKey: (key: string) => void;
  updateSettings: (settings: Partial<AgentSettings>) => void;
  setTokenUsage: (usage: number) => void;
  clearMessages: () => void;
}

export const useAgentStore = create<AgentStore>((set) => ({
  messages: [],
  sessions: [],
  currentSessionId: null,
  isThinking: false,
  isStreaming: false,
  apiKey: localStorage.getItem('claude_api_key'),
  settings: {
    model: 'claude-3-5-sonnet-20241022',
    temperature: 0.7,
    maxTokens: 4096,
    systemPrompt: 'You are a helpful coding assistant. You help users write, debug, and understand code.',
  },
  tokenUsage: 0,

  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setSessions: (sessions) => set({ sessions }),
  setCurrentSessionId: (id) => set({ currentSessionId: id }),
  setIsThinking: (thinking) => set({ isThinking: thinking }),
  setIsStreaming: (streaming) => set({ isStreaming: streaming }),
  setApiKey: (key) => {
    localStorage.setItem('claude_api_key', key);
    set({ apiKey: key });
  },
  updateSettings: (newSettings) => set((state) => ({
    settings: { ...state.settings, ...newSettings }
  })),
  setTokenUsage: (usage) => set({ tokenUsage: usage }),
  clearMessages: () => set({ messages: [] }),
}));
