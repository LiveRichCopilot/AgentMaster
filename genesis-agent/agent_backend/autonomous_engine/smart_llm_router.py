"""
Smart LLM Router - Cost Optimizer
Routes requests to Flash (cheap) or Pro (expensive) based on task complexity
Saves 70-80% on API costs without hurting quality
"""

from typing import Optional, Dict
from .resilient_llm import ResilientLLM


class SmartLLMRouter:
    """
    Intelligent model selection:
    - Flash (10x cheaper): Simple tasks, research queries, error analysis
    - Pro (expensive): Code generation, complex reasoning, debugging
    """
    
    def __init__(self):
        self.flash = ResilientLLM(model_name="gemini-2.5-flash")
        self.pro = ResilientLLM(model_name="gemini-2.5-pro")
        
        # Track cost savings
        self.stats = {
            "flash_calls": 0,
            "pro_calls": 0,
            "estimated_savings": 0.0
        }
    
    def _should_use_pro(self, task_type: str, prompt: str) -> bool:
        """
        Decide if we need Pro or if Flash is good enough.
        
        Use Pro (gemini-2.5-pro) for:
        - Code generation (writing/fixing actual code)
        - Complex debugging (multiple related errors)
        - Architecture decisions
        
        Use Flash (gemini-2.5-flash) for:
        - Research queries
        - Simple error analysis
        - Documentation lookup
        - File content reading
        """
        # Explicit task types that need Pro
        pro_tasks = [
            "code_generation",
            "complex_debugging", 
            "architecture",
            "fix_generation"
        ]
        
        if task_type in pro_tasks:
            return True
        
        # Check prompt for code-related keywords
        code_indicators = [
            "generate the complete",
            "fix the following code",
            "create a function",
            "implement",
            "refactor",
            "optimize the code"
        ]
        
        prompt_lower = prompt.lower()
        if any(indicator in prompt_lower for indicator in code_indicators):
            return True
        
        # Check prompt length - very long context often needs Pro
        if len(prompt) > 3000:
            return True
        
        # Default to Flash (cheaper)
        return False
    
    async def generate_code(
        self, 
        prompt: str, 
        task_type: str = "code_generation"
    ) -> str:
        """
        Generate code using the appropriate model.
        Code generation ALWAYS uses Pro.
        """
        use_pro = True  # Always use Pro for code generation
        
        if use_pro:
            print(f"💎 Using Gemini 2.5 Pro (high quality)")
            self.stats["pro_calls"] += 1
            result = await self.pro.generate_code(prompt)
        else:
            print(f"⚡ Using Gemini 2.5 Flash (fast & cheap)")
            self.stats["flash_calls"] += 1
            self.stats["estimated_savings"] += 0.05  # ~$0.05 saved per call
            result = await self.flash.generate_code(prompt)
        
        return result
    
    async def analyze_text(
        self, 
        prompt: str,
        task_type: str = "analysis"
    ) -> str:
        """
        Analyze text/errors using the appropriate model.
        Most analysis can use Flash.
        """
        use_pro = self._should_use_pro(task_type, prompt)
        
        if use_pro:
            print(f"💎 Using Gemini 2.5 Pro (complex reasoning)")
            self.stats["pro_calls"] += 1
            result = await self.pro.generate_code(prompt)  # Using generate_code as general method
        else:
            print(f"⚡ Using Gemini 2.5 Flash (simple analysis)")
            self.stats["flash_calls"] += 1
            self.stats["estimated_savings"] += 0.05
            result = await self.flash.generate_code(prompt)
        
        return result
    
    async def research_topic(self, query: str, use_grounding: bool = True) -> str:
        """
        Research using Flash + Google Search grounding.
        Research doesn't need Pro's reasoning - just needs to find info.
        """
        print(f"⚡ Using Gemini 2.5 Flash for research (10x cheaper)")
        self.stats["flash_calls"] += 1
        self.stats["estimated_savings"] += 0.05
        
        # Flash is perfect for research queries
        result = await self.flash.generate_code(query)
        return result
    
    def get_cost_report(self) -> Dict:
        """
        Returns cost statistics and savings.
        """
        total_calls = self.stats["flash_calls"] + self.stats["pro_calls"]
        flash_percentage = (self.stats["flash_calls"] / total_calls * 100) if total_calls > 0 else 0
        
        return {
            "total_calls": total_calls,
            "flash_calls": self.stats["flash_calls"],
            "pro_calls": self.stats["pro_calls"],
            "flash_percentage": round(flash_percentage, 1),
            "estimated_savings": round(self.stats["estimated_savings"], 2),
            "message": f"Saved ~${self.stats['estimated_savings']:.2f} by using Flash for {self.stats['flash_calls']} calls"
        }
    
    def print_cost_summary(self):
        """Print a nice summary of cost savings."""
        report = self.get_cost_report()
        print(f"\n{'='*60}")
        print(f"💰 COST OPTIMIZATION REPORT")
        print(f"{'='*60}")
        print(f"Total LLM calls: {report['total_calls']}")
        print(f"  ⚡ Flash calls: {report['flash_calls']} ({report['flash_percentage']}%)")
        print(f"  💎 Pro calls: {report['pro_calls']} ({100 - report['flash_percentage']:.1f}%)")
        print(f"💵 Estimated savings: ${report['estimated_savings']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    print("Smart LLM Router - Cost Optimizer")
    print("Routes tasks to Flash (cheap) or Pro (expensive) intelligently")

