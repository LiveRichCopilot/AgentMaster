"""
Demo test - Shows Phase 2 with LLM disabled (Phase 1 fallback)
This demonstrates the system works even without Gemini
"""

import asyncio
from pathlib import Path
from autonomous_engine import AutonomousEngine


async def demo_test():
    """
    Demo: Run autonomous engine with LLM disabled
    This will use Phase 1 pattern-based execution
    """
    print("\n" + "="*70)
    print("DEMO TEST - Autonomous Engine (Phase 1 Fallback Mode)")
    print("="*70)
    
    workspace = Path(__file__).parent / "demo_workspace"
    workspace.mkdir(exist_ok=True)
    
    # Initialize with LLM disabled
    engine = AutonomousEngine(workspace_dir=str(workspace), use_llm=False)
    
    result = await engine.run(
        goal="Create a file called demo.txt"
    )
    
    print(f"\n✅ Test Result: {result}")
    
    # Verify the file
    demo_file = workspace / "demo.txt"
    if demo_file.exists():
        print(f"\n✅ SUCCESS! File created: {demo_file}")
        print(f"\n📄 Content:\n")
        print(demo_file.read_text())
    else:
        print(f"\n❌ File not created")
    
    return result


if __name__ == "__main__":
    asyncio.run(demo_test())
