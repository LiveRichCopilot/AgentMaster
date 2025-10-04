"""
Cognitive Supervisor: The Learning Mind
This implements JAi's architecture for true autonomous learning.

Components:
1. StateTracker - Remembers what has been tried
2. StrategyEngine - Decides on new approaches when stuck
3. CognitiveSupervisor - Orchestrates the learning loop
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AttemptRecord:
    """Record of a single autonomous attempt."""
    attempt_number: int
    strategy: str
    error: Optional[str]
    success: bool
    timestamp: datetime


class StateTracker:
    """
    The Memory: Remembers what has been tried.
    Implements "I've seen this before" capability.
    """
    
    def __init__(self):
        self.history: List[AttemptRecord] = []
    
    def log_attempt(self, attempt_details: Dict):
        """Logs the result of one attempt."""
        record = AttemptRecord(
            attempt_number=attempt_details['attempt'],
            strategy=attempt_details['strategy'],
            error=attempt_details.get('error'),
            success=attempt_details['success'],
            timestamp=datetime.now()
        )
        self.history.append(record)
        
        # Print status
        status = "✅ SUCCESS" if record.success else f"❌ FAILED: {record.error[:100] if record.error else 'Unknown'}"
        print(f"📊 Attempt {record.attempt_number} ({record.strategy}): {status}")
    
    def detect_loop(self, lookback: int = 3) -> bool:
        """
        Checks if the same error has occurred multiple times in a row.
        This is the implementation of "knowing you can't do that way again."
        """
        if len(self.history) < lookback:
            return False
        
        # Get the last few attempts using the same strategy
        recent_attempts = self.history[-lookback:]
        
        # Check if all failed with similar errors
        if not all(not attempt.success for attempt in recent_attempts):
            return False  # Some succeeded, not a loop
        
        # Check if they all used the same strategy
        strategies = [attempt.strategy for attempt in recent_attempts]
        if len(set(strategies)) != 1:
            return False  # Different strategies, not a loop
        
        # Get error signatures
        recent_errors = [self._error_signature(attempt.error) for attempt in recent_attempts]
        
        # If all recent errors have the same signature, we are in a loop
        first_error = recent_errors[0]
        if all(error == first_error for error in recent_errors):
            print(f"\n🧠 LOOP DETECTED: Same error repeated {lookback} times with strategy '{strategies[0]}'")
            print(f"   Error pattern: {first_error}")
            return True
        
        return False
    
    def _error_signature(self, error: Optional[str]) -> str:
        """
        Creates a simplified signature of an error for comparison.
        This helps detect when the same type of error keeps happening.
        """
        if not error:
            return "no_error"
        
        # Simplified signature (first 50 chars, lowercased, no whitespace)
        signature = error.lower().replace(" ", "")[:50]
        return signature
    
    def get_summary(self) -> Dict:
        """Returns a summary of all attempts."""
        total = len(self.history)
        successes = sum(1 for a in self.history if a.success)
        failures = total - successes
        
        strategies_used = list(set(a.strategy for a in self.history))
        
        return {
            "total_attempts": total,
            "successes": successes,
            "failures": failures,
            "strategies_used": strategies_used
        }


class StrategyEngine:
    """
    The Creative Problem-Solver: Decides on new approaches when stuck.
    Implements "try something else" capability.
    """
    
    def __init__(self):
        self.strategies = [
            {
                "name": "direct_file_fix",
                "description": "Fix the most likely file based on error keywords",
                "complexity": 1
            },
            {
                "name": "contextual_file_fix",
                "description": "Provide multiple related files to LLM for context",
                "complexity": 2
            },
            {
                "name": "use_template",
                "description": "Use a proven template instead of generating from scratch",
                "complexity": 2
            },
            {
                "name": "rebuild_backend",
                "description": "Rebuild backend from scratch to match frontend expectations",
                "complexity": 3
            },
            {
                "name": "web_search_for_solution",
                "description": "Search the web for solutions to this specific error",
                "complexity": 4
            }
        ]
        self.current_strategy_index = 0
    
    def get_current_strategy(self) -> Dict:
        """Returns the current best strategy."""
        return self.strategies[self.current_strategy_index]
    
    def change_strategy(self) -> bool:
        """
        Switches to a more advanced strategy.
        This is the implementation of "trying another way."
        
        Returns:
            bool: True if strategy changed, False if exhausted all strategies
        """
        if self.current_strategy_index < len(self.strategies) - 1:
            self.current_strategy_index += 1
            new_strategy = self.strategies[self.current_strategy_index]
            print(f"\n💡 STRATEGY CHANGE: Escalating to '{new_strategy['name']}'")
            print(f"   Reason: Current approach is not working")
            print(f"   New approach: {new_strategy['description']}")
            return True
        else:
            print("\n❌ STRATEGY EXHAUSTED: All known strategies have been tried")
            return False
    
    def reset(self):
        """Resets to the first strategy."""
        self.current_strategy_index = 0


class CognitiveSupervisor:
    """
    The Main Loop of Learning.
    Orchestrates StateTracker and StrategyEngine to achieve true autonomy.
    
    This is the "consciousness" that watches the agent work, remembers,
    and decides when to try a different approach.
    """
    
    def __init__(self, executor):
        """
        Args:
            executor: The object that actually runs the build/deploy/verify
                      (e.g., MetaAppBuilder instance)
        """
        self.state_tracker = StateTracker()
        self.strategy_engine = StrategyEngine()
        self.executor = executor
        self.max_attempts = 999999  # No artificial limits - keep going until it works!
    
    async def run_autonomous_flow(self):
        """
        The main loop of autonomous learning.
        
        This is where the magic happens:
        1. Try current strategy
        2. Remember the outcome
        3. Detect if stuck in a loop
        4. If stuck, change strategy
        5. Repeat until success or all strategies exhausted
        """
        print("\n" + "=" * 60)
        print("🧠 COGNITIVE SUPERVISOR ACTIVATED")
        print("=" * 60)
        print("This system will:")
        print("  • Remember every attempt")
        print("  • Detect when stuck in a loop")
        print("  • Try different approaches automatically")
        print("  • Search the web when needed")
        print("=" * 60 + "\n")
        
        attempt = 0
        while attempt < self.max_attempts:
            attempt += 1
            
            # 1. Get the current strategy
            current_strategy = self.strategy_engine.get_current_strategy()
            print(f"\n🚀 ATTEMPT {attempt}/{self.max_attempts}")
            print(f"   Strategy: {current_strategy['name']}")
            print(f"   {current_strategy['description']}")
            
            # 2. Execute the strategy and verify the result
            try:
                success, error = await self.executor.run_with_strategy(
                    strategy=current_strategy['name']
                )
            except Exception as e:
                success = False
                error = str(e)
            
            # 3. Log the outcome to memory
            self.state_tracker.log_attempt({
                'attempt': attempt,
                'strategy': current_strategy['name'],
                'error': error,
                'success': success
            })
            
            # 4. Check for success
            if success:
                print("\n" + "=" * 60)
                print("🎉 SUCCESS! Goal achieved.")
                print("=" * 60)
                self._print_summary()
                return True
            
            # 5. If failed, check for a loop to trigger self-correction
            if self.state_tracker.detect_loop(lookback=3):
                # This is the moment of learning: change the approach
                strategy_changed = self.strategy_engine.change_strategy()
                
                if not strategy_changed:
                    # We've tried everything we know
                    print("\n" + "=" * 60)
                    print("❌ FAILED: Exhausted all known strategies")
                    print("=" * 60)
                    self._print_summary()
                    return False
        
        print("\n" + "=" * 60)
        print(f"❌ FAILED: Could not achieve goal after {self.max_attempts} attempts")
        print("=" * 60)
        self._print_summary()
        return False
    
    def _print_summary(self):
        """Prints a summary of the autonomous session."""
        summary = self.state_tracker.get_summary()
        print("\n📊 SESSION SUMMARY:")
        print(f"   Total attempts: {summary['total_attempts']}")
        print(f"   Successes: {summary['successes']}")
        print(f"   Failures: {summary['failures']}")
        print(f"   Strategies used: {', '.join(summary['strategies_used'])}")


# Example usage
if __name__ == "__main__":
    print("Cognitive Supervisor Test")
    print("This module provides the learning architecture.")
    print("Run meta_app_builder_v3.py to see it in action.")

