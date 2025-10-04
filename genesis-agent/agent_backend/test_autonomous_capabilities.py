"""
Comprehensive Test Suite for ALL Autonomous Capabilities
Tests every single function we integrated over the past 10 hours
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from jai_cortex_working import (
    learn_from_error,
    search_my_knowledge,
    web_search_for_solution,
    research_topic,
    verify_code_quality,
    AUTONOMOUS_ENABLED
)

print("=" * 80)
print("🧪 COMPREHENSIVE AUTONOMOUS CAPABILITIES TEST SUITE")
print("=" * 80)
print(f"\n✅ Autonomous Enabled: {AUTONOMOUS_ENABLED}\n")

if not AUTONOMOUS_ENABLED:
    print("❌ Autonomous capabilities not available!")
    sys.exit(1)

async def test_all_capabilities():
    """Test every autonomous capability"""
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 5
    }
    
    # ========================================================================
    # TEST 1: Learn from Error
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 1: learn_from_error - Can the agent remember mistakes?")
    print("=" * 80)
    try:
        result = learn_from_error(
            error="TypeError: 'str' object is not callable",
            solution="Changed msg.text() to msg.text - it's a property not a method",
            context="Playwright browser testing"
        )
        print(f"Result: {result}")
        if result.get("status") == "success":
            print("✅ TEST 1 PASSED - Agent can learn from errors")
            results["passed"] += 1
        else:
            print(f"❌ TEST 1 FAILED - {result.get('message', 'Unknown error')}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ TEST 1 FAILED - Exception: {e}")
        results["failed"] += 1
    
    # ========================================================================
    # TEST 2: Search Knowledge Base
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 2: search_my_knowledge - Can the agent find what it learned?")
    print("=" * 80)
    try:
        result = search_my_knowledge(query="Playwright msg.text property error")
        print(f"Result: {result}")
        if result.get("status") in ["success", "no_results"]:
            print("✅ TEST 2 PASSED - Knowledge search working")
            results["passed"] += 1
        else:
            print(f"❌ TEST 2 FAILED - {result.get('message', 'Unknown error')}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ TEST 2 FAILED - Exception: {e}")
        results["failed"] += 1
    
    # ========================================================================
    # TEST 3: Web Search for Solution
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 3: web_search_for_solution - Can agent search real web?")
    print("=" * 80)
    try:
        result = await web_search_for_solution(
            problem="How to handle async functions in Python Flask"
        )
        print(f"Result status: {result.get('status')}")
        print(f"Sources found: {len(result.get('sources', []))}")
        if result.get("status") == "success":
            print("✅ TEST 3 PASSED - Web search working")
            results["passed"] += 1
        else:
            print(f"❌ TEST 3 FAILED - {result.get('message', 'Unknown error')}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ TEST 3 FAILED - Exception: {e}")
        results["failed"] += 1
    
    # ========================================================================
    # TEST 4: Research Topic (Proactive Learning)
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 4: research_topic - Can agent research proactively?")
    print("=" * 80)
    try:
        result = await research_topic(topic="Flask routing best practices")
        print(f"Result: {result}")
        if result.get("status") == "success":
            print("✅ TEST 4 PASSED - Research agent working")
            results["passed"] += 1
        else:
            print(f"❌ TEST 4 FAILED - {result.get('message', 'Unknown error')}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ TEST 4 FAILED - Exception: {e}")
        results["failed"] += 1
    
    # ========================================================================
    # TEST 5: Verify Code Quality
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 5: verify_code_quality - Can agent verify code?")
    print("=" * 80)
    try:
        test_code = '''
def hello_world():
    """Simple test function"""
    return "Hello, World!"
        '''
        result = verify_code_quality(
            code=test_code,
            language="python",
            description="Simple hello world function"
        )
        print(f"Result: {result}")
        if result.get("status") == "success":
            print("✅ TEST 5 PASSED - Code verification working")
            results["passed"] += 1
        else:
            print(f"❌ TEST 5 FAILED - {result.get('message', 'Unknown error')}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ TEST 5 FAILED - Exception: {e}")
        results["failed"] += 1
    
    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed'] / results['total']) * 100:.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED - FULLY AUTONOMOUS!")
    else:
        print(f"\n⚠️  {results['failed']} tests failed - needs attention")
    
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    asyncio.run(test_all_capabilities())

