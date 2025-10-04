"""
Test script for autonomous engine components
Tests TaskManager and EnvironmentTools before building the main loop
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from .task_manager import Task, TaskManager
from environment_tools import EnvironmentTools
import uuid


def test_task_manager():
    """Test the TaskManager component."""
    print("\n" + "="*60)
    print("TESTING: TaskManager")
    print("="*60 + "\n")
    
    # Create task manager
    tm = TaskManager(goal="Test the task management system")
    
    # Create some test tasks
    tasks = [
        Task(id=str(uuid.uuid4()), description="Task 1: Create a file"),
        Task(id=str(uuid.uuid4()), description="Task 2: Run a command"),
        Task(id=str(uuid.uuid4()), description="Task 3: Update the file"),
    ]
    
    # Add tasks
    tm.add_tasks(tasks)
    
    # Show progress
    print(f"\n{tm}")
    print(f"Pending tasks: {tm.has_pending_tasks()}")
    
    # Execute tasks
    while tm.has_pending_tasks():
        task = tm.get_next_task()
        
        # Simulate success
        if "Task 1" in task.description or "Task 3" in task.description:
            tm.mark_completed(task, {'status': 'success'})
        else:
            # Simulate failure for Task 2
            tm.mark_failed(task, "Simulated error")
    
    # Show final progress
    print(f"\n{tm}")
    summary = tm.get_progress_summary()
    print(f"\n📊 Final Summary:")
    print(f"   Completed: {summary['completed']}")
    print(f"   Failed: {len(tm.failed_tasks)}")
    print(f"   Progress: {summary['progress_percentage']:.1f}%")
    
    print("\n✅ TaskManager test passed!\n")


def test_environment_tools():
    """Test the EnvironmentTools component."""
    print("\n" + "="*60)
    print("TESTING: EnvironmentTools")
    print("="*60 + "\n")
    
    # Create test workspace
    test_workspace = Path(__file__).parent / "test_workspace"
    env = EnvironmentTools(workspace_dir=str(test_workspace))
    
    # Test 1: Create a file
    print("Test 1: Creating a file...")
    result = env.create_file("test.txt", "Hello from autonomous engine!")
    assert result['success'], f"Failed to create file: {result.get('error')}"
    print(f"✅ {result['message']}\n")
    
    # Test 2: Read the file
    print("Test 2: Reading the file...")
    result = env.read_file("test.txt")
    assert result['success'], f"Failed to read file: {result.get('error')}"
    assert result['content'] == "Hello from autonomous engine!", "Content mismatch"
    print(f"✅ Read {result['lines']} lines ({result['size_bytes']} bytes)\n")
    
    # Test 3: Update the file
    print("Test 3: Updating the file...")
    result = env.update_file("test.txt", "Hello from autonomous engine!\nUpdated content!")
    assert result['success'], f"Failed to update file: {result.get('error')}"
    print(f"✅ {result['message']}\n")
    
    # Test 4: List files
    print("Test 4: Listing files...")
    result = env.list_files()
    assert result['success'], f"Failed to list files: {result.get('error')}"
    print(f"✅ Found {result['total_items']} items: {result['files']}\n")
    
    # Test 5: Run a command
    print("Test 5: Running a command...")
    result = env.run_command("echo 'Command test'")
    assert result['success'], f"Failed to run command: {result.get('error')}"
    print(f"✅ Command output: {result['stdout'].strip()}\n")
    
    # Show operations log
    print("📋 Operations performed:")
    for i, op in enumerate(env.get_operations_log(), 1):
        print(f"   {i}. {op['operation']}: {op['details']}")
    
    print("\n✅ EnvironmentTools test passed!\n")


def main():
    """Run all component tests."""
    print("\n" + "🔬 AUTONOMOUS ENGINE - COMPONENT TESTS" + "\n")
    
    try:
        # Test TaskManager
        test_task_manager()
        
        # Test EnvironmentTools
        test_environment_tools()
        
        print("="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("1. ✅ TaskManager working")
        print("2. ✅ EnvironmentTools working")
        print("3. 🔄 Ready to build the Execution Loop (autonomous_engine.py)")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

