"""
Web-Assisted Learning System for Autonomous Agent
This module implements the ability to search for solutions when stuck.
"""

import re
import asyncio
from typing import Dict, Optional, List, Tuple
from google import genai
from google.genai import types as genai_types


class WebLearner:
    """
    Implements web-based learning when the agent encounters unknown errors.
    This is the 'phone a friend' capability.
    """

    def __init__(self):
        """Initialize the web learner with Gemini integration."""
        try:
            # Use Vertex AI authentication
            self.client = genai.Client(
                vertexai=True,
                project="studio-2416451423-f2d96",
                location="us-central1"
            )
            print("✅ WebLearner initialized with Vertex AI")
        except Exception as e:
            print(f"⚠️ WebLearner init error: {e}")
            self.client = None

    async def search_for_solution(
        self,
        error_message: str,
        tech_stack: List[str],
        current_file_content: str,
        current_file_path: str,
    ) -> Optional[Dict]:
        """
        Main orchestration method: search web, analyze, and propose a fix.

        Args:
            error_message: The error that the agent is stuck on
            tech_stack: List of technologies (e.g., ['Python', 'Flask'])
            current_file_content: The code that's causing the error
            current_file_path: Path to the file (for context)

        Returns:
            Dict with 'fixed_code', 'explanation', 'source_url'
        """
        if not self.client:
            return None

        print("\n🔍 WEB-ASSISTED LEARNING ACTIVATED")
        print("=" * 60)

        # Step 1: Formulate a high-quality search query
        query = self._formulate_query(error_message, tech_stack)

        # Step 2: Execute web search (simulated for now)
        search_results = await self._execute_search(query)

        # Step 3: Synthesize a solution from the top results
        solution = await self._synthesize_solution(
            error_message,
            search_results,
            current_file_content,
            current_file_path
        )

        return solution

    def _formulate_query(
        self, error_message: str, tech_stack: List[str]
    ) -> str:
        """
        Step 1: Transform raw error into an effective search query.

        Logic:
        - Extract core error (last line of traceback)
        - Remove file paths (project-specific noise)
        - Add technology keywords
        """
        # Get the last line (usually the most important)
        lines = error_message.strip().splitlines()
        core_error = lines[-1] if lines else error_message

        # Remove file paths like "/Users/.../app.py"
        core_error = re.sub(r"/[\w/\-\.]+\.py", "", core_error)

        # Remove line numbers like "line 123"
        core_error = re.sub(r"line \d+", "", core_error)

        # Add tech stack keywords
        query = f"{core_error} {' '.join(tech_stack)}"

        print(f"📝 Formulated query: {query}")
        return query

    async def _execute_search(self, query: str) -> List[Dict]:
        """
        Step 2: Execute web search and return ranked results.
        Now uses REAL Gemini grounding for actual web results.
        """
        print(f"🌐 Searching REAL web for: {query}")

        if not self.client:
            return []

        try:
            # Use Gemini with Google Search grounding for REAL results
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model="gemini-2.0-flash-exp",
                contents=genai_types.Part.from_text(
                    text=f"Search the web for: {query}\n\nProvide 3-5 relevant URLs with titles and brief descriptions of each result."
                ),
                config=genai_types.GenerateContentConfig(
                    tools=[genai_types.Tool(google_search={})]  # Enable Google Search
                )
            )

            # Parse response to extract URLs
            results = self._parse_search_response(response.text, query)
            
            if results:
                print(f"✅ Found {len(results)} REAL web sources")
                return results
            else:
                print("⚠️ No results from web search, falling back to Gemini knowledge")
                return self._fallback_results(query)

        except Exception as e:
            print(f"⚠️ Web search error: {e}, using Gemini's knowledge")
            return self._fallback_results(query)

    def _parse_search_response(self, response_text: str, query: str) -> List[Dict]:
        """Parse Gemini's search response to extract URLs."""
        results = []
        
        # Simple parsing - look for URLs in the response
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, response_text)
        
        for url in urls[:5]:  # Take top 5
            results.append({
                "url": url,
                "title": f"Web result for: {query[:50]}...",
                "snippet": "Found via Google Search grounding"
            })
        
        return results

    def _fallback_results(self, query: str) -> List[Dict]:
        """Fallback when web search fails - use Gemini's training knowledge."""
        return [
            {
                "url": "https://playwright.dev/python/docs/selectors",
                "title": "Playwright Selectors Documentation",
                "snippet": "Fallback: Playwright selector best practices"
            },
            {
                "url": "https://stackoverflow.com/questions/tagged/playwright",
                "title": "Stack Overflow - Playwright Questions",
                "snippet": "Fallback: Common Playwright solutions"
            }
        ]
    
    async def _synthesize_solution(
        self,
        error_message: str,
        search_results: List[Dict],
        current_file_content: str,
        current_file_path: str,
    ) -> Optional[Dict]:
        """
        Step 3 & 4: Use LLM to synthesize a solution from web results
        and apply it to the actual code.
        """
        if not self.client:
            return None

        print("🧠 Synthesizing solution from web knowledge...")

        # Build the prompt
        prompt = f"""You are a senior software engineer with access to web search results.

**THE ERROR:**
{error_message}

**THE FILE THAT NEEDS FIXING:**
File: {current_file_path}
```
{current_file_content}
```

**WEB SEARCH RESULTS:**
{self._format_search_results(search_results)}

**YOUR TASK:**
1. Analyze the error in the context of the provided code
2. Use insights from the web search results to understand the root cause
3. Generate the COMPLETE, CORRECTED version of the file

**CRITICAL REQUIREMENTS:**
- Output ONLY the complete, fixed code
- Do NOT include explanations, markdown, or comments about the fix
- The code must be syntactically correct and runnable
- Fix the specific error while preserving all other functionality

Generate the corrected code now:"""

        try:
            # Call Gemini in a separate thread to avoid blocking
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model="gemini-2.0-flash-exp",
                contents=genai_types.Part.from_text(text=prompt),
            )

            fixed_code = response.text.strip()

            # Remove markdown code blocks if present
            fixed_code = self._clean_code_response(fixed_code)

            print("✅ Solution synthesized from web knowledge")

            return {
                "fixed_code": fixed_code,
                "explanation": "Fix generated using web-assisted learning",
                "source_url": search_results[0]["url"] if search_results else "N/A",
            }

        except Exception as e:
            print(f"❌ Error synthesizing solution: {e}")
            return None

    def _clean_code_response(self, code: str) -> str:
        """
        Clean LLM response by removing markdown code blocks.
        Extracted for better separation of concerns.
        """
        if code.startswith("```"):
            lines = code.split("\n")
            # Remove first and last lines (```)
            code = "\n".join(lines[1:-1])
        return code

    def _format_search_results(self, results: List[Dict]) -> str:
        """Format search results for LLM prompt."""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result['title']}")
            formatted.append(f"   URL: {result['url']}")
            formatted.append(f"   {result['snippet']}")
        return "\n".join(formatted)


# Example usage
async def test_web_learner():
    """Test the web learner with a sample error."""
    learner = WebLearner()
    
    sample_error = """
Traceback (most recent call last):
  File "/Users/test/app.py", line 45, in run
    result = self.diagnose_and_
AttributeError: 'MetaAppBuilder' object has no attribute 'diagnose_and_'. Did you mean: 'diagnose_and_fix'?
"""
    
    sample_code = """
class MetaAppBuilder:
    def run(self):
        result = self.diagnose_and_()
"""
    
    solution = await learner.search_for_solution(
        error_message=sample_error,
        tech_stack=["Python", "Flask"],
        current_file_content=sample_code,
        current_file_path="meta_app_builder.py"
    )
    
    if solution:
        print("\n" + "=" * 60)
        print("SOLUTION FOUND:")
        print(solution['explanation'])
        print(f"Source: {solution['source_url']}")
        print("\nFixed Code:")
        print(solution['fixed_code'])


if __name__ == "__main__":
    asyncio.run(test_web_learner())

