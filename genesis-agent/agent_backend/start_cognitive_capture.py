#!/usr/bin/env python3
"""
Cognitive Capture Background Service
Monitors conversations and automatically captures them for cognitive modeling

Run this alongside your ADK server to enable automatic cognitive profiling.

Usage:
    python start_cognitive_capture.py
"""

import time
import sqlite3
import json
from pathlib import Path
from jai_cortex.cognitive_middleware import cognitive_middleware

# Session database path
SESSION_DB = Path(__file__).parent / "jai_cortex_sessions.db"

# Track processed messages
processed_messages = set()


def monitor_sessions():
    """Monitor the session database and auto-capture new conversations"""
    print("🧠 Cognitive Capture Service Started")
    print(f"📊 Monitoring: {SESSION_DB}")
    print(f"✅ Auto-capture: {'ENABLED' if cognitive_middleware.enabled else 'DISABLED'}")
    print("-" * 60)
    
    while True:
        try:
            # Connect to session database
            conn = sqlite3.connect(str(SESSION_DB))
            cursor = conn.cursor()
            
            # Query for session messages (adjust based on actual schema)
            # This is a simplified example - actual implementation depends on ADK's session structure
            cursor.execute("""
                SELECT session_id, user_id, content 
                FROM sessions 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                session_id, user_id, content_json = row
                message_id = f"{session_id}:{user_id}"
                
                if message_id not in processed_messages:
                    try:
                        # Parse message content
                        content = json.loads(content_json)
                        messages = content.get('messages', [])
                        
                        # Find user-agent message pairs
                        for i in range(len(messages) - 1):
                            if messages[i]['role'] == 'user' and messages[i+1]['role'] == 'assistant':
                                user_message = messages[i]['content']
                                agent_response = messages[i+1]['content']
                                
                                # Auto-capture
                                result = cognitive_middleware.capture_conversation(
                                    user_id=user_id or 'default_user',
                                    session_id=session_id,
                                    user_message=user_message,
                                    agent_response=agent_response
                                )
                                
                                if result['status'] == 'success':
                                    print(f"✅ Captured: {session_id[:8]}... (#{result['capture_count']})")
                                
                        processed_messages.add(message_id)
                        
                    except json.JSONDecodeError:
                        pass
                    except Exception as e:
                        print(f"⚠️  Error processing message: {e}")
            
            conn.close()
            
        except sqlite3.OperationalError as e:
            # Database might not exist yet
            if "no such table" in str(e):
                print(f"⏳ Waiting for session database to be created...")
            else:
                print(f"⚠️  Database error: {e}")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
        
        # Wait before next check
        time.sleep(2)


if __name__ == "__main__":
    try:
        monitor_sessions()
    except KeyboardInterrupt:
        print("\n\n🛑 Cognitive Capture Service Stopped")
        stats = cognitive_middleware.get_stats()
        print(f"📊 Total Captured: {stats['total_captured']}")

