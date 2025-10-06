export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isCode?: boolean;
  codeLanguage?: string;
  toolUsed?: string;
}

export interface AgentStatus {
  online: boolean;
  thinking: boolean;
  responding: boolean;
  currentTool?: string;
}

export interface Session {
  id: string;
  name: string;
  createdAt: Date;
  lastMessage?: Date;
}

export interface VoiceSettings {
  enabled: boolean;
  pitch: number;
  rate: number;
  volume: number;
  voice?: string;
}

export interface CodeExecution {
  code: string;
  language: string;
  output?: string;
  error?: string;
}
