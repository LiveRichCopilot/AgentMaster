"""
Multi-Platform Webhook Handlers
Telegram, WhatsApp, SMS integrations
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
import os

router = APIRouter()

# ============================================================================
# TELEGRAM WEBHOOK
# ============================================================================

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """
    Telegram Bot Webhook
    
    Setup:
    1. Create bot with @BotFather
    2. Get bot token
    3. Set webhook: https://api.telegram.org/bot<TOKEN>/setWebhook?url=<YOUR_URL>/webhook/telegram
    """
    try:
        data = await request.json()
        
        # Extract message
        if 'message' not in data:
            return {'status': 'ok'}
        
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        user_id = message['from']['id']
        
        # Import here to avoid circular imports
        from multi_agent_system import get_router
        from server import chat_with_agent
        
        # Route to appropriate agent
        router_result = get_router().handle_message(
            message=text,
            platform='telegram',
            user_id=str(user_id),
            session_id=str(chat_id)
        )
        
        # Get response from agent
        response = await chat_with_agent(text, str(chat_id), str(user_id))
        
        # Send reply via Telegram
        await send_telegram_message(chat_id, response['response'])
        
        return {'status': 'ok'}
        
    except Exception as e:
        print(f"Telegram webhook error: {e}")
        return {'status': 'error', 'message': str(e)}


async def send_telegram_message(chat_id: int, text: str):
    """Send message via Telegram Bot API"""
    import httpx
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        })


# ============================================================================
# WHATSAPP WEBHOOK (Twilio)
# ============================================================================

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    WhatsApp Webhook via Twilio
    
    Setup:
    1. Create Twilio account
    2. Get WhatsApp sandbox or verified sender
    3. Set webhook URL in Twilio console
    """
    try:
        form_data = await request.form()
        
        # Extract Twilio WhatsApp message
        from_number = form_data.get('From', '')
        body = form_data.get('Body', '')
        message_sid = form_data.get('MessageSid', '')
        
        # Import here to avoid circular imports
        from multi_agent_system import get_router
        from server import chat_with_agent
        
        # Route to appropriate agent
        router_result = get_router().handle_message(
            message=body,
            platform='whatsapp',
            user_id=from_number,
            session_id=message_sid
        )
        
        # Get response from agent
        response = await chat_with_agent(body, message_sid, from_number)
        
        # Send reply via WhatsApp (Twilio)
        await send_whatsapp_message(from_number, response['response'])
        
        return {'status': 'ok'}
        
    except Exception as e:
        print(f"WhatsApp webhook error: {e}")
        return {'status': 'error', 'message': str(e)}


async def send_whatsapp_message(to_number: str, message: str):
    """Send WhatsApp message via Twilio"""
    from twilio.rest import Client
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    
    if not account_sid or not auth_token:
        print("⚠️  Twilio credentials not set")
        return
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=from_number,
            body=message,
            to=to_number
        )
        
        print(f"✅ WhatsApp sent: {message.sid}")
    except Exception as e:
        print(f"❌ WhatsApp send error: {e}")


# ============================================================================
# PROACTIVE ALERTS
# ============================================================================

async def send_proactive_alert(user_id: str, message: str, platforms: list = ['web', 'telegram', 'whatsapp']):
    """
    Send proactive alert to user across platforms
    
    Args:
        user_id: User identifier
        message: Alert message
        platforms: List of platforms to send to
    """
    results = {}
    
    if 'telegram' in platforms:
        # Look up user's telegram chat_id (would need to store this)
        chat_id = get_user_telegram_id(user_id)
        if chat_id:
            await send_telegram_message(chat_id, f"🔔 {message}")
            results['telegram'] = 'sent'
    
    if 'whatsapp' in platforms:
        # Look up user's phone number
        phone = get_user_phone(user_id)
        if phone:
            await send_whatsapp_message(f"whatsapp:{phone}", f"🔔 {message}")
            results['whatsapp'] = 'sent'
    
    if 'web' in platforms:
        # Store in database for web notification
        # Would use WebSocket or SSE to push to browser
        results['web'] = 'queued'
    
    return results


def get_user_telegram_id(user_id: str) -> int:
    """Get user's Telegram chat ID from database"""
    # In production, look this up from Firestore
    # For now, return None
    return None


def get_user_phone(user_id: str) -> str:
    """Get user's phone number from database"""
    # In production, look this up from Firestore
    # For now, return None
    return None


# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================

SETUP_INSTRUCTIONS = """
# 🔌 MULTI-PLATFORM SETUP

## Telegram Setup (5 min)
1. Open Telegram, search for @BotFather
2. Send /newbot and follow instructions
3. Copy the bot token
4. Add to .env: TELEGRAM_BOT_TOKEN=your_token_here
5. Set webhook:
   ```bash
   curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
     -d "url=https://your-domain.com/webhook/telegram"
   ```

## WhatsApp Setup (10 min via Twilio)
1. Create Twilio account: https://www.twilio.com/try-twilio
2. Get WhatsApp sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
3. Add to .env:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```
4. Set webhook in Twilio console to: https://your-domain.com/webhook/whatsapp

## Environment Variables Needed
```bash
# Telegram
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=<your_twilio_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Test
- Telegram: Message your bot
- WhatsApp: Send message to Twilio number
- Web: Already working at http://localhost:5173
"""
