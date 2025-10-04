"""
Meta-Memory System - Phase 2.8
The system's knowledge base of errors and solutions
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MetaMemory:
    """
    Stores and retrieves solutions to problems
    The system's long-term memory of what works
    """
    
    def __init__(self, memory_file: str = "meta_memory.json"):
        self.memory_file = Path(__file__).parent / memory_file
        self.memory = self.load_memory()
        
    def load_memory(self) -> Dict:
        """Load existing memory or create new"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return self.create_new_memory()
        else:
            return self.create_new_memory()
    
    def create_new_memory(self) -> Dict:
        """Create new memory structure"""
        return {
            "solutions": {},
            "patterns": {},
            "statistics": {
                "total_errors_seen": 0,
                "total_solutions_saved": 0,
                "total_reuses": 0
            }
        }
    
    def save_memory(self):
        """Persist memory to disk"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def has_seen_error(self, error_signature: str) -> bool:
        """
        Check if we've encountered this error before
        
        Args:
            error_signature: Unique identifier for the error
            
        Returns:
            True if we have a solution for this error
        """
        return error_signature in self.memory["solutions"]
    
    def get_solution(self, error_signature: str) -> Optional[Dict]:
        """
        Retrieve a known solution for this error
        
        Args:
            error_signature: The error we're trying to fix
            
        Returns:
            Solution dict or None if not found
        """
        if self.has_seen_error(error_signature):
            solution = self.memory["solutions"][error_signature]
            
            # Track reuse
            solution["reuse_count"] = solution.get("reuse_count", 0) + 1
            solution["last_reused"] = datetime.now().isoformat()
            self.memory["statistics"]["total_reuses"] += 1
            self.save_memory()
            
            return solution
        return None
    
    def save_solution(self, error_signature: str, solution: Dict):
        """
        Save a solution that worked
        
        Args:
            error_signature: The error pattern
            solution: The fix that worked
        """
        self.memory["solutions"][error_signature] = {
            "solution": solution,
            "first_seen": datetime.now().isoformat(),
            "reuse_count": 0,
            "success_rate": 1.0
        }
        
        self.memory["statistics"]["total_errors_seen"] += 1
        self.memory["statistics"]["total_solutions_saved"] += 1
        self.save_memory()
        
        print(f"💾 Solution saved to memory: {error_signature}")
    
    def create_error_signature(self, error_type: str, file_path: str, error_message: str) -> str:
        """
        Create a unique signature for an error
        This allows pattern matching
        
        Args:
            error_type: Type of error (e.g., "missing_file", "empty_file")
            file_path: The file with the error
            error_message: The error message
            
        Returns:
            Unique signature string
        """
        # Normalize the signature
        if "too small" in error_message.lower() or "empty" in error_message.lower():
            return f"empty_file:{file_path}"
        
        if "missing" in error_message.lower():
            # Extract what's missing (e.g., "Missing: Chat container (selector: #chat-container)")
            if "selector:" in error_message:
                selector = error_message.split("selector:")[1].strip().rstrip(")")
                return f"missing_element:{selector}"
            return f"missing:{file_path}"
        
        # Generic signature
        return f"{error_type}:{file_path}"
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        return {
            **self.memory["statistics"],
            "known_solutions": len(self.memory["solutions"]),
            "memory_file": str(self.memory_file)
        }
    
    def clear_memory(self):
        """Clear all memory (use with caution!)"""
        self.memory = self.create_new_memory()
        self.save_memory()
        print("🧹 Memory cleared")

