import Anthropic from '@anthropic-ai/sdk';

export interface ClaudeMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface StreamResponse {
  text: string;
  done: boolean;
}

class ClaudeService {
  private client: Anthropic | null = null;

  initialize(apiKey: string) {
    this.client = new Anthropic({
      apiKey,
      dangerouslyAllowBrowser: true,
    });
  }

  isInitialized(): boolean {
    return !!this.client;
  }

  async *streamMessage(
    messages: ClaudeMessage[],
    model: string = 'claude-3-5-sonnet-20241022',
    maxTokens: number = 4096,
    temperature: number = 0.7
  ): AsyncGenerator<StreamResponse> {
    if (!this.client) {
      throw new Error('Claude client not initialized. Call initialize() with API key first.');
    }

    const stream = await this.client.messages.create({
      model,
      max_tokens: maxTokens,
      temperature,
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content,
      })),
      stream: true,
    });

    let fullText = '';

    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
        fullText += event.delta.text;
        yield {
          text: fullText,
          done: false,
        };
      }
    }

    yield {
      text: fullText,
      done: true,
    };
  }

  async sendMessage(
    messages: ClaudeMessage[],
    model: string = 'claude-3-5-sonnet-20241022',
    maxTokens: number = 4096,
    temperature: number = 0.7
  ): Promise<string> {
    if (!this.client) {
      throw new Error('Claude client not initialized. Call initialize() with API key first.');
    }

    const response = await this.client.messages.create({
      model,
      max_tokens: maxTokens,
      temperature,
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content,
      })),
    });

    const textContent = response.content.find(block => block.type === 'text');
    return textContent && textContent.type === 'text' ? textContent.text : '';
  }
}

export const claudeService = new ClaudeService();
