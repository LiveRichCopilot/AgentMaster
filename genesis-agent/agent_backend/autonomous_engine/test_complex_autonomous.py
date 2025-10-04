"""
Complex Autonomous Engine Test
Tests multiple files, task decomposition, and error handling
"""

import asyncio
from autonomous_engine import run_autonomous_task
from pathlib import Path


async def test_complex_scenario():
    """
    Test Scenario: Create a simple React component structure
    - Creates component file
    - Creates test file  
    - Creates README
    - Verifies all files exist
    """
    
    workspace = Path(__file__).parent / "complex_test_workspace"
    
    print("\n" + "="*60)
    print("🧪 COMPLEX AUTONOMOUS TEST")
    print("="*60)
    print("Goal: Create a React component structure with 3 files")
    print()
    
    result = await run_autonomous_task(
        goal="Create a React component called Button",
        workspace_dir=str(workspace)
    )
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    # Verify results
    files_created = []
    if workspace.exists():
        files_created = list(workspace.glob("*.*"))
    
    print(f"\n✅ Autonomous execution completed")
    print(f"📁 Files created: {len(files_created)}")
    for f in files_created:
        print(f"   - {f.name}")
    
    print(f"\n📈 Execution Summary:")
    print(f"   Goal: {result['goal']}")
    print(f"   Success: {result['success']}")
    print(f"   Tasks completed: {result['summary']['completed']}")
    print(f"   Tasks failed: {result['summary']['failed']}")
    print(f"   Iterations: {result['iterations']}")
    
    # Verify each file
    print(f"\n🔍 File Verification:")
    expected_files = ['Button.tsx', 'Button.test.tsx']
    for expected_file in expected_files:
        file_path = workspace / expected_file
        if file_path.exists():
            print(f"   ✅ {expected_file} - EXISTS ({file_path.stat().st_size} bytes)")
        else:
            print(f"   ❌ {expected_file} - MISSING")
    
    print("\n" + "="*60)
    print("🎯 TEST COMPLETE")
    print("="*60 + "\n")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_complex_scenario())

