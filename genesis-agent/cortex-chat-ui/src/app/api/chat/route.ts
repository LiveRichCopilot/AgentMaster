import { NextRequest, NextResponse } from 'next/server';

const META_AGENT_API = process.env.NEXT_PUBLIC_META_AGENT_API || 'http://localhost:8080';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Forward to MetaAgent API
    const response = await fetch(`${META_AGENT_API}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: body.message,
        conversation_history: body.conversation_history || [],
        session_id: body.session_id || 'default'
      }),
    });

    if (!response.ok) {
      throw new Error(`MetaAgent API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    return NextResponse.json({
      response: data.response,
      agent_used: data.agent_used,
      success: data.success
    });
    
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Failed to process chat request' },
      { status: 500 }
    );
  }
}

export async function GET() {
  // Health check
  try {
    const response = await fetch(`${META_AGENT_API}/agents`);
    const data = await response.json();
    
    return NextResponse.json({
      status: 'ok',
      agents: data
    });
  } catch (error) {
    return NextResponse.json(
      { status: 'error', error: String(error) },
      { status: 500 }
    );
  }
}
