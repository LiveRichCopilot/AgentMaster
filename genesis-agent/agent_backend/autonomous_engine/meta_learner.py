"""
Meta-Learner System - Phase 2.8
Detects patterns, applies known solutions, and learns from failures
"""

from typing import Dict, List, Optional, Tuple
from .meta_memory import MetaMemory


class MetaLearner:
    """
    The intelligence layer that:
    1. Recognizes errors it's seen before
    2. Applies known solutions immediately
    3. Detects when it's stuck in a loop
    4. Triggers self-improvement when needed
    """
    
    def __init__(self):
        self.memory = MetaMemory()
        self.current_run_errors = []
        self.loop_detection_threshold = 3  # If same error 3 times = stuck
        
    def analyze_error(self, errors: List[str], files_state: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Analyze an error and decide what to do
        
        Args:
            errors: List of error messages
            files_state: Current state of files (which exist, their sizes)
            
        Returns:
            (has_known_solution, solution_dict)
        """
        print(f"\n{'='*70}")
        print(f"🧠 META-LEARNER: Analyzing Error")
        print(f"{'='*70}\n")
        
        # Track this error
        self.current_run_errors.append(errors)
        
        # Check if we're stuck in a loop
        if self.is_stuck_in_loop():
            print(f"🔄 LOOP DETECTED: Same error repeated {self.loop_detection_threshold} times")
            print(f"🔧 Triggering self-improvement protocol...")
            return (False, {"trigger_self_improvement": True})
        
        # Analyze each error
        for error in errors:
            # Create error signature
            signature = self.create_signature_from_error(error)
            
            print(f"🔍 Error signature: {signature}")
            
            # Check memory
            if self.memory.has_seen_error(signature):
                solution = self.memory.get_solution(signature)
                
                print(f"💡 KNOWN ERROR! I've seen this before.")
                print(f"📊 This solution has been reused {solution['reuse_count']} times")
                print(f"✅ Applying saved solution...")
                
                return (True, solution)
            else:
                print(f"🆕 NEW ERROR: I haven't seen this before")
                print(f"🤖 Will attempt to solve with Gemini...")
                
                return (False, {"error_signature": signature})
        
        return (False, None)
    
    def save_successful_solution(
        self, 
        error_signature: str, 
        solution_data: Dict
    ):
        """
        Save a solution that worked
        
        Args:
            error_signature: The error pattern
            solution_data: What fixed it (file content, approach, etc.)
        """
        print(f"\n{'='*70}")
        print(f"💾 META-LEARNER: Saving Successful Solution")
        print(f"{'='*70}\n")
        
        self.memory.save_solution(error_signature, solution_data)
        
        # Clear error history for this run (we fixed it!)
        self.current_run_errors = []
        
        stats = self.memory.get_statistics()
        print(f"📊 Memory Stats:")
        print(f"   • Total errors learned: {stats['known_solutions']}")
        print(f"   • Total reuses: {stats['total_reuses']}")
        print(f"   • Success: Faster next time! ⚡\n")
    
    def create_signature_from_error(self, error: str) -> str:
        """
        Create error signature for pattern matching
        IMPROVED: Creates composite signatures for multiple related errors
        
        Args:
            error: Error message string
            
        Returns:
            Unique signature
        """
        error_lower = error.lower()
        
        # Pattern: File too small/empty
        if "too small" in error_lower or "empty" in error_lower:
            if "requirements.txt" in error_lower:
                return "empty_file:requirements.txt"
            if "index.html" in error_lower:
                return "empty_file:templates/index.html"
            if "style.css" in error_lower:
                return "empty_file:static/style.css"
            if "script.js" in error_lower:
                return "empty_file:static/script.js"
        
        # Pattern: Missing UI elements (multiple at once = HTML structure problem)
        if "missing:" in error_lower:
            # Check for multiple missing elements = broken HTML template
            missing_count = error_lower.count("missing:")
            if missing_count >= 2:
                # Multiple elements missing = HTML template needs fixing
                return "broken_html_template:multiple_missing_elements"
            
            # Single missing element
            if "#chat-container" in error_lower:
                return "missing_element:#chat-container"
            if "#message-form" in error_lower:
                return "missing_element:#message-form"
            if "#message-input" in error_lower:
                return "missing_element:#message-input"
        
        # Pattern: JavaScript errors (often caused by missing HTML)
        if "javascript" in error_lower or "js error" in error_lower or "error:" in error_lower:
            # If there are also missing elements, it's a broken HTML issue
            if "missing:" in error_lower or "chat" in error_lower:
                return "broken_html_template:multiple_missing_elements"
            return "js_error:console"
        
        # Generic fallback
        return f"generic_error:{error[:50]}"
    
    def is_stuck_in_loop(self) -> bool:
        """
        Detect if we're making the same mistake repeatedly
        
        Returns:
            True if stuck in a loop
        """
        if len(self.current_run_errors) < self.loop_detection_threshold:
            return False
        
        # Check last N errors
        recent_errors = self.current_run_errors[-self.loop_detection_threshold:]
        
        # If they're all the same, we're stuck
        first_error_signature = str(recent_errors[0])
        
        for error_list in recent_errors[1:]:
            if str(error_list) != first_error_signature:
                return False
        
        return True
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about what the system has learned"""
        stats = self.memory.get_statistics()
        
        return {
            **stats,
            "current_run_errors": len(self.current_run_errors),
            "stuck_in_loop": self.is_stuck_in_loop()
        }
    
    def reset_run(self):
        """Reset for a new run"""
        self.current_run_errors = []
        print("🔄 Meta-Learner: Ready for new run\n")

