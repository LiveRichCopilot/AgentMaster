#!/usr/bin/env python3
"""
Test Cognitive Modeling System
Demonstrates automatic conversation capture and cognitive profiling
"""

from jai_cortex.memory_service import memory_service

def test_auto_capture():
    """Test automatic conversation capture with context detection"""
    print("🧠 COGNITIVE MODELING TEST")
    print("=" * 60)
    
    # Test conversations with different contexts
    test_conversations = [
        {
            'context': 'Agency Business',
            'user': 'I need help creating a marketing campaign for our new client',
            'agent': 'I can help you design a comprehensive marketing campaign. What is the client\'s industry and target audience?'
        },
        {
            'context': 'Travel Business',
            'user': 'Can you help me optimize our hotel booking flow?',
            'agent': 'I\'d be happy to help optimize your booking process. Let\'s analyze the current user journey...'
        },
        {
            'context': 'Development',
            'user': 'How do I fix this database error in my Python code?',
            'agent': 'Let me help you debug that. Can you share the error message and relevant code?'
        },
        {
            'context': 'Personal',
            'user': 'I feel overwhelmed with all these projects',
            'agent': 'I understand. Let\'s break down your projects and prioritize them step by step.'
        }
    ]
    
    # Capture each conversation
    for i, conv in enumerate(test_conversations, 1):
        print(f"\n📝 Test {i}: {conv['context']}")
        print(f"   User: {conv['user'][:50]}...")
        
        doc_id = memory_service.auto_capture_conversation(
            user_id="test_user",
            session_id=f"test_session_{i}",
            user_message=conv['user'],
            agent_response=conv['agent']
        )
        
        if doc_id:
            print(f"   ✅ Captured: {doc_id}")
        else:
            print(f"   ❌ Failed to capture")
    
    print("\n" + "=" * 60)
    
    # Get cognitive profile
    print("\n📊 COGNITIVE PROFILE ANALYSIS")
    print("=" * 60)
    
    profile = memory_service.get_cognitive_profile(user_id="test_user", days=1)
    
    print(f"\n📈 Analysis Period: {profile['analysis_period_days']} days")
    print(f"💬 Total Conversations: {profile['total_conversations']}")
    
    if profile['total_conversations'] > 0:
        print(f"\n🎯 Primary Contexts:")
        for context, count in profile['primary_contexts'].items():
            print(f"   - {context}: {count} conversations")
        
        print(f"\n💭 Communication Styles:")
        for style, count in profile['communication_styles'].items():
            print(f"   - {style}: {count} times")
        
        if profile['key_topics']:
            print(f"\n🔑 Key Topics:")
            for topic, count in profile['key_topics'].items():
                print(f"   - {topic}: mentioned {count} times")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("\nNext Steps:")
    print("1. Check Firestore 'conversation_memory' collection")
    print("2. Ask JAi: 'Show me my cognitive profile'")
    print("3. Start having conversations - the system learns automatically!")


if __name__ == "__main__":
    try:
        test_auto_capture()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

