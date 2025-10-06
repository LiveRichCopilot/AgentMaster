import type { Message, CodeExecution } from '../types';

const ADK_BASE_URL = 'http://127.0.0.1:8000';

class ADKService {
  private ws: WebSocket | null = null;
  private messageHandlers: ((message: Message) => void)[] = [];
  private statusHandlers: ((status: any) => void)[] = [];

  connect() {
    const wsUrl = ADK_BASE_URL.replace('http', 'ws') + '/api/stream';

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('Connected to ADK Agent');
        this.notifyStatus({ online: true, thinking: false, responding: false });
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === 'message') {
            const message: Message = {
              id: Date.now().toString(),
              role: 'assistant',
              content: data.content,
              timestamp: new Date(),
              toolUsed: data.tool
            };
            this.messageHandlers.forEach(handler => handler(message));
          } else if (data.type === 'status') {
            this.notifyStatus(data.status);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.notifyStatus({ online: false, thinking: false, responding: false });
      };

      this.ws.onclose = () => {
        console.log('Disconnected from ADK Agent');
        this.notifyStatus({ online: false, thinking: false, responding: false });
        setTimeout(() => this.connect(), 5000);
      };
    } catch (error) {
      console.error('Failed to connect to ADK:', error);
      this.notifyStatus({ online: false, thinking: false, responding: false });
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  async sendMessage(content: string): Promise<Message> {
    try {
      const response = await fetch(`${ADK_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: content }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response || data.message,
        timestamp: new Date(),
      };
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async executeCode(code: string, language: string): Promise<CodeExecution> {
    try {
      const response = await fetch(`${ADK_BASE_URL}/api/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, language }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        code,
        language,
        output: data.output,
        error: data.error,
      };
    } catch (error) {
      console.error('Error executing code:', error);
      return {
        code,
        language,
        error: error instanceof Error ? error.message : 'Failed to execute code',
      };
    }
  }

  async getSessions() {
    try {
      const response = await fetch(`${ADK_BASE_URL}/api/sessions`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching sessions:', error);
      return [];
    }
  }

  onMessage(handler: (message: Message) => void) {
    this.messageHandlers.push(handler);
    return () => {
      this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
    };
  }

  onStatus(handler: (status: any) => void) {
    this.statusHandlers.push(handler);
    return () => {
      this.statusHandlers = this.statusHandlers.filter(h => h !== handler);
    };
  }

  private notifyStatus(status: any) {
    this.statusHandlers.forEach(handler => handler(status));
  }
}

export const adkService = new ADKService();
