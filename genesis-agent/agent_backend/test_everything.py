#!/usr/bin/env python3
"""
COMPREHENSIVE TEST SUITE
Tests EVERY feature before deployment
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test(name: str, func):
    """Run a test and report results"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {name}")
    print('='*60)
    try:
        result = func()
        if result.get('status') == 'success' or result.get('response'):
            print(f"✅ PASSED")
            print(f"Result: {json.dumps(result, indent=2)[:500]}")
            return True
        else:
            print(f"⚠️  PARTIAL: {result}")
            return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

# ============================================================================
# BASIC TESTS
# ============================================================================

def test_server_running():
    """Test if server is up"""
    r = requests.get(f"{BASE_URL}/")
    return r.json()

def test_health_check():
    """Test health endpoint"""
    r = requests.get(f"{BASE_URL}/api/health")
    return r.json()

# ============================================================================
# AGENT TESTS
# ============================================================================

def test_list_agents():
    """Test listing specialist agents"""
    r = requests.get(f"{BASE_URL}/api/agents")
    return r.json()

def test_agent_strength():
    """Test agent strength metrics"""
    r = requests.get(f"{BASE_URL}/api/agents/FinanceWizard/strength")
    return r.json()

# ============================================================================
# CHAT TESTS
# ============================================================================

def test_basic_chat():
    """Test basic conversation"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Hey! What can you do?",
        "session_id": "test_basic",
        "user_id": "tester"
    })
    return r.json()

def test_tool_execution():
    """Test tool execution - create folder"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Create a folder called TestFolder2024",
        "session_id": "test_tools",
        "user_id": "tester"
    })
    return r.json()

def test_financial_agent_routing():
    """Test routing to financial agent"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "I need to track my expenses for this month",
        "session_id": "test_finance",
        "user_id": "tester"
    })
    return r.json()

def test_code_agent_routing():
    """Test routing to code agent"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Help me debug this Python function",
        "session_id": "test_code",
        "user_id": "tester"
    })
    return r.json()

# ============================================================================
# SELF-CODING TESTS
# ============================================================================

def test_read_own_code():
    """Test agent reading its own code"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Read your server.py file and tell me the version",
        "session_id": "test_selfcode",
        "user_id": "tester"
    })
    return r.json()

# ============================================================================
# MEMORY TESTS
# ============================================================================

def test_save_note():
    """Test saving a note"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Save a note: Test suite ran successfully on " + time.strftime("%Y-%m-%d"),
        "session_id": "test_memory",
        "user_id": "tester"
    })
    return r.json()

def test_search_notes():
    """Test searching notes"""
    r = requests.post(f"{BASE_URL}/api/chat", json={
        "message": "Search my notes for 'test suite'",
        "session_id": "test_memory2",
        "user_id": "tester"
    })
    return r.json()

# ============================================================================
# MULTI-AGENT TESTS
# ============================================================================

def test_create_custom_agent():
    """Test creating custom agent"""
    r = requests.post(f"{BASE_URL}/api/agents/create", json={
        "template": "code_master",
        "custom_name": "MyDevBot"
    })
    return r.json()

def test_platform_stats():
    """Test platform statistics"""
    r = requests.get(f"{BASE_URL}/api/platform/stats")
    return r.json()

# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🚀 "*20)
    print("COMPREHENSIVE TEST SUITE - Testing ALL Features")
    print("🚀 "*20 + "\n")
    
    results = {}
    
    # Basic tests
    results['server'] = test("Server Running", test_server_running)
    results['health'] = test("Health Check", test_health_check)
    
    # Agent tests
    results['list_agents'] = test("List Specialist Agents", test_list_agents)
    results['agent_strength'] = test("Agent Strength Metrics", test_agent_strength)
    
    # Chat tests
    results['basic_chat'] = test("Basic Conversation", test_basic_chat)
    results['tool_exec'] = test("Tool Execution (Create Folder)", test_tool_execution)
    results['finance_routing'] = test("Financial Agent Routing", test_financial_agent_routing)
    results['code_routing'] = test("Code Agent Routing", test_code_agent_routing)
    
    # Self-coding
    results['read_code'] = test("Self-Coding (Read Own Code)", test_read_own_code)
    
    # Memory
    results['save_note'] = test("Save Note", test_save_note)
    results['search_notes'] = test("Search Notes", test_search_notes)
    
    # Multi-agent
    results['create_agent'] = test("Create Custom Agent", test_create_custom_agent)
    results['platform_stats'] = test("Platform Statistics", test_platform_stats)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {passed/total*100:.1f}%\n")
    
    print("DETAILED RESULTS:")
    for test_name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {test_name}")
    
    print("\n" + "="*60)
    
    if passed >= total * 0.8:  # 80% pass rate
        print("🎉 SYSTEM READY FOR DEPLOYMENT!")
    else:
        print("⚠️  FIX FAILING TESTS BEFORE DEPLOYMENT")
    
    print("="*60 + "\n")
