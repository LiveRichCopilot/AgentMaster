"""
Phase 2 Test - LLM-Powered Autonomous Execution
Tests the Gemini-integrated autonomous engine
"""

import asyncio
import os
from pathlib import Path
from autonomous_engine import AutonomousEngine


async def test_simple_component():
    """
    Test 1: Simple React component generation
    This tests if Gemini can decompose the goal and generate real React code
    """
    print("\n" + "="*70)
    print("TEST 1: Simple React Component")
    print("="*70)
    
    workspace = Path(__file__).parent / "phase2_test_workspace"
    workspace.mkdir(exist_ok=True)
    
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=True)
    
    result = await engine.run(
        goal="Create a React Button component with TypeScript"
    )
    
    print(f"\n✅ Test 1 Result: {result}")
    
    # Verify the file was created
    button_file = workspace / "Button.tsx"
    if button_file.exists():
        print(f"✅ File created: {button_file}")
        print(f"\n📄 Generated code:\n")
        print(button_file.read_text())
    else:
        print(f"❌ File not created: {button_file}")
    
    return result


async def test_component_with_tests():
    """
    Test 2: Component with tests
    Tests if Gemini can create both component and test files
    """
    print("\n" + "="*70)
    print("TEST 2: Component with Tests")
    print("="*70)
    
    workspace = Path(__file__).parent / "phase2_test_workspace"
    workspace.mkdir(exist_ok=True)
    
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=True)
    
    result = await engine.run(
        goal="Create a React Card component with tests"
    )
    
    print(f"\n✅ Test 2 Result: {result}")
    
    # Verify files were created
    component_file = workspace / "Card.tsx"
    test_file = workspace / "Card.test.tsx"
    
    for file in [component_file, test_file]:
        if file.exists():
            print(f"✅ File created: {file.name}")
            print(f"\n📄 Content:\n")
            print(file.read_text())
            print("\n" + "-"*70 + "\n")
        else:
            print(f"❌ File not created: {file.name}")
    
    return result


async def test_python_function():
    """
    Test 3: Python function generation
    Tests if Gemini can work with different languages
    """
    print("\n" + "="*70)
    print("TEST 3: Python Function")
    print("="*70)
    
    workspace = Path(__file__).parent / "phase2_test_workspace"
    workspace.mkdir(exist_ok=True)
    
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=True)
    
    result = await engine.run(
        goal="Create a Python function that calculates fibonacci numbers with type hints and docstrings"
    )
    
    print(f"\n✅ Test 3 Result: {result}")
    
    # Look for Python files
    py_files = list(workspace.glob("*.py"))
    if py_files:
        for py_file in py_files:
            if py_file.name != "test_phase2.py":  # Skip this test file
                print(f"✅ File created: {py_file.name}")
                print(f"\n📄 Content:\n")
                print(py_file.read_text())
    else:
        print(f"❌ No Python files created")
    
    return result


async def test_complex_feature():
    """
    Test 4: More complex feature
    Tests if Gemini can handle multi-file features
    """
    print("\n" + "="*70)
    print("TEST 4: Complex Feature - Login Form")
    print("="*70)
    
    workspace = Path(__file__).parent / "phase2_test_workspace"
    workspace.mkdir(exist_ok=True)
    
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=True)
    
    result = await engine.run(
        goal="Create a React login form with email validation and error handling"
    )
    
    print(f"\n✅ Test 4 Result: {result}")
    
    # List all files created
    all_files = [f for f in workspace.iterdir() if f.is_file() and f.suffix in ['.tsx', '.ts']]
    print(f"\n📁 Files created: {len(all_files)}")
    for file in all_files:
        print(f"  - {file.name} ({file.stat().st_size} bytes)")
    
    return result


async def run_all_tests():
    """
    Run all Phase 2 tests
    """
    print("\n" + "🚀"*35)
    print("PHASE 2 AUTONOMOUS ENGINE TESTS")
    print("Testing LLM-Powered Execution with Gemini 2.5 Pro (Vertex AI)")
    print("🚀"*35)
    
    print("\n✅ Using Vertex AI authentication (same as JAi Cortex)")
    print("📍 Project: studio-2416451423-f2d96")
    print("📍 Location: us-central1\n")
    
    results = []
    
    try:
        # Test 1: Simple component
        result1 = await test_simple_component()
        results.append(("Simple Component", result1))
        await asyncio.sleep(1)  # Small delay between tests
        
        # Test 2: Component with tests
        result2 = await test_component_with_tests()
        results.append(("Component with Tests", result2))
        await asyncio.sleep(1)
        
        # Test 3: Python function
        result3 = await test_python_function()
        results.append(("Python Function", result3))
        await asyncio.sleep(1)
        
        # Test 4: Complex feature (optional - takes longer)
        # Uncomment to run:
        # result4 = await test_complex_feature()
        # results.append(("Complex Feature", result4))
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*70)
    print("PHASE 2 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        success = result.get('success', False)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"       Tasks: {result['summary']['completed']}/{result['summary']['total_tasks']}")
        print(f"       Iterations: {result['iterations']}")
    
    print("\n" + "="*70)
    print(f"Total tests run: {len(results)}")
    print(f"Passed: {sum(1 for _, r in results if r.get('success'))}")
    print(f"Failed: {sum(1 for _, r in results if not r.get('success'))}")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())

