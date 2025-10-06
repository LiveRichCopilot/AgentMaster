import { createClient, SupabaseClient } from '@supabase/supabase-js';

export interface SessionData {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface MessageData {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

class SupabaseService {
  private client: SupabaseClient | null = null;

  initialize(url: string, anonKey: string) {
    this.client = createClient(url, anonKey);
  }

  async getSessions(): Promise<SessionData[]> {
    if (!this.client) return [];

    const { data, error } = await this.client
      .from('conversations')
      .select('*')
      .order('updated_at', { ascending: false });

    if (error) {
      console.error('Error fetching sessions:', error);
      return [];
    }

    return data || [];
  }

  async createSession(title: string = 'New Conversation'): Promise<SessionData | null> {
    if (!this.client) return null;

    const { data, error } = await this.client
      .from('conversations')
      .insert({ title })
      .select()
      .single();

    if (error) {
      console.error('Error creating session:', error);
      return null;
    }

    return data;
  }

  async getMessages(sessionId: string): Promise<MessageData[]> {
    if (!this.client) return [];

    const { data, error } = await this.client
      .from('messages')
      .select('*')
      .eq('conversation_id', sessionId)
      .order('created_at', { ascending: true });

    if (error) {
      console.error('Error fetching messages:', error);
      return [];
    }

    return data || [];
  }

  async saveMessage(sessionId: string, role: 'user' | 'assistant', content: string): Promise<void> {
    if (!this.client) return;

    const { error } = await this.client
      .from('messages')
      .insert({
        conversation_id: sessionId,
        role,
        content,
      });

    if (error) {
      console.error('Error saving message:', error);
    }

    await this.updateSessionTimestamp(sessionId);
  }

  async updateSessionTitle(sessionId: string, title: string): Promise<void> {
    if (!this.client) return;

    const { error } = await this.client
      .from('conversations')
      .update({ title, updated_at: new Date().toISOString() })
      .eq('id', sessionId);

    if (error) {
      console.error('Error updating session title:', error);
    }
  }

  async deleteSession(sessionId: string): Promise<void> {
    if (!this.client) return;

    const { error} = await this.client
      .from('conversations')
      .delete()
      .eq('id', sessionId);

    if (error) {
      console.error('Error deleting session:', error);
    }
  }

  private async updateSessionTimestamp(sessionId: string): Promise<void> {
    if (!this.client) return;

    const { error } = await this.client
      .from('conversations')
      .update({ updated_at: new Date().toISOString() })
      .eq('id', sessionId);

    if (error) {
      console.error('Error updating session timestamp:', error);
    }
  }
}

export const supabaseService = new SupabaseService();
