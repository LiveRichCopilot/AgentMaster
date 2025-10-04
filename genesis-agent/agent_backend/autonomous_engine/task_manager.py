"""
Task Manager - Core component of the Autonomous Engine
Manages the task queue, tracks completion, and maintains working state.

Phase 1: Simple Implementation
- Task queue (FIFO)
- Completion tracking
- Basic state management
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class Task:
    """Represents a single task in the autonomous execution."""
    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error': self.error,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries
        }


class TaskManager:
    """
    Manages the task queue and execution state for autonomous operation.
    
    Key Responsibilities:
    - Maintain task queue (what needs to be done)
    - Track completed tasks (what's been done)
    - Store working state (files created, commands run, etc.)
    - Provide task to execute next
    """
    
    def __init__(self, goal: str):
        self.goal = goal
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self.working_state: Dict[str, Any] = {
            'files_created': [],
            'files_modified': [],
            'commands_run': [],
            'tests_passed': [],
            'errors_encountered': []
        }
        self.current_task: Optional[Task] = None
        
    def add_task(self, task: Task) -> None:
        """Add a new task to the queue."""
        self.task_queue.append(task)
        print(f"📝 Task added: {task.description}")
        
    def add_tasks(self, tasks: List[Task]) -> None:
        """Add multiple tasks to the queue."""
        for task in tasks:
            self.add_task(task)
            
    def get_next_task(self) -> Optional[Task]:
        """Get the next task from the queue."""
        if not self.task_queue:
            return None
            
        self.current_task = self.task_queue.pop(0)
        self.current_task.status = "in_progress"
        print(f"▶️  Starting task: {self.current_task.description}")
        return self.current_task
        
    def mark_completed(self, task: Task, result: Dict[str, Any]) -> None:
        """Mark a task as completed."""
        task.status = "completed"
        task.completed_at = datetime.now()
        task.result = result
        self.completed_tasks.append(task)
        print(f"✅ Task completed: {task.description}")
        
    def mark_failed(self, task: Task, error: str) -> None:
        """Mark a task as failed."""
        task.error = error
        task.retry_count += 1
        
        if task.retry_count < task.max_retries:
            # Retry: Put back in queue at front
            task.status = "pending"
            self.task_queue.insert(0, task)
            print(f"🔄 Task failed, retrying ({task.retry_count}/{task.max_retries}): {task.description}")
        else:
            # Max retries exceeded
            task.status = "failed"
            self.failed_tasks.append(task)
            print(f"❌ Task failed permanently: {task.description} - {error}")
            
    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update the working state with new information."""
        for key, value in updates.items():
            if key in self.working_state and isinstance(self.working_state[key], list):
                self.working_state[key].append(value)
            else:
                self.working_state[key] = value
                
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of current progress."""
        total_tasks = len(self.completed_tasks) + len(self.failed_tasks) + len(self.task_queue)
        if self.current_task:
            total_tasks += 1
            
        return {
            'goal': self.goal,
            'total_tasks': total_tasks,
            'completed': len(self.completed_tasks),
            'failed': len(self.failed_tasks),
            'pending': len(self.task_queue),
            'current_task': self.current_task.description if self.current_task else None,
            'progress_percentage': (len(self.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        }
        
    def has_pending_tasks(self) -> bool:
        """Check if there are any pending tasks."""
        return len(self.task_queue) > 0
        
    def save_state(self, filepath: str) -> None:
        """Save the current state to a file."""
        state = {
            'goal': self.goal,
            'task_queue': [task.to_dict() for task in self.task_queue],
            'completed_tasks': [task.to_dict() for task in self.completed_tasks],
            'failed_tasks': [task.to_dict() for task in self.failed_tasks],
            'working_state': self.working_state,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
        print(f"💾 State saved to {filepath}")
        
    def __repr__(self) -> str:
        summary = self.get_progress_summary()
        return f"TaskManager(goal='{self.goal}', progress={summary['progress_percentage']:.1f}%, completed={summary['completed']}, pending={summary['pending']})"

