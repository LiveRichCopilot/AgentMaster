"""
Proactive Research Agent
Researches topics BEFORE execution to build knowledge.
"""

import asyncio
from typing import List, Dict
from google import genai
from google.genai import types as genai_types
from .knowledge_base import KnowledgeBase


class ResearchAgent:
    """
    Proactively researches topics to build knowledge before execution.
    
    This is the difference between:
    - Reactive: Try → Fail → Search
    - Proactive: Research → Build Knowledge → Execute with Intelligence
    """
    
    def __init__(self):
        """Initialize research agent with Gemini Flash (10x cheaper!) and knowledge base."""
        self.kb = KnowledgeBase()
        self.model_name = "gemini-2.5-flash"  # Use Flash for research - way cheaper!
        
        try:
            self.client = genai.Client(
                vertexai=True,
                project="studio-2416451423-f2d96",
                location="us-central1"
            )
            print("✅ Research Agent initialized (using Gemini 2.5 Flash for 10x cost savings)")
        except Exception as e:
            print(f"⚠️ Research Agent init error: {e}")
            self.client = None
    
    async def research_goal(self, goal: str) -> Dict:
        """
        Research a goal BEFORE attempting to execute it.
        
        This builds knowledge about:
        - Technologies needed
        - Best practices
        - Common pitfalls
        - Proven patterns
        
        Args:
            goal: The high-level goal (e.g., "Build a Flask chat app")
        
        Returns:
            Dict with research findings and knowledge stored
        """
        print("\n" + "="*70)
        print("🔬 PROACTIVE RESEARCH PHASE")
        print("="*70)
        print(f"Goal: {goal}")
        print("="*70 + "\n")
        
        # Step 1: Identify topics to research
        topics = await self._identify_topics(goal)
        print(f"📋 Identified {len(topics)} topics to research:")
        for topic in topics:
            print(f"   • {topic}")
        print()
        
        # Step 2: Research each topic
        findings = {}
        for i, topic in enumerate(topics, 1):
            print(f"🔍 Researching ({i}/{len(topics)}): {topic}...")
            try:
                knowledge = await self._research_topic(topic)
                if knowledge:
                    findings[topic] = knowledge
                    # Store in knowledge base
                    self.kb.add_topic_knowledge(
                        topic=topic,
                        knowledge=knowledge,
                        source="proactive_research"
                    )
                    print(f"   ✅ Success")
                await asyncio.sleep(3)  # Increased delay to avoid rate limits
            except Exception as e:
                print(f"   ⚠️ Skipped due to rate limit: {str(e)[:50]}...")
                await asyncio.sleep(5)  # Longer delay after error
        
        # Step 3: Identify best practices
        print(f"\n📚 Identifying best practices...")
        best_practices = await self._identify_best_practices(goal, topics)
        for tech, practices in best_practices.items():
            for practice in practices:
                self.kb.add_best_practice(
                    technology=tech,
                    practice=practice["practice"],
                    rationale=practice["rationale"]
                )
        
        # Step 4: Identify common pitfalls
        print(f"\n⚠️ Identifying common pitfalls...")
        pitfalls = await self._identify_pitfalls(goal, topics)
        for pitfall in pitfalls:
            self.kb.add_pattern(
                pattern_name=pitfall["name"],
                description=pitfall["description"],
                solution=pitfall["solution"]
            )
        
        print("\n" + "="*70)
        print("✅ RESEARCH COMPLETE")
        self.kb.print_summary()
        
        return {
            "topics": topics,
            "findings": findings,
            "best_practices": best_practices,
            "pitfalls": pitfalls
        }
    
    async def _identify_topics(self, goal: str) -> List[str]:
        """Identify what topics need to be researched for this goal."""
        if not self.client:
            return []
        
        prompt = f"""You are a research assistant preparing for a coding task.

Task: {goal}

Identify 5-7 specific technical topics that should be researched before attempting this task.

Examples of good topics:
- "Flask route handlers and return values"
- "Playwright selector best practices"
- "HTML form submission with JavaScript"
- "Flask static file serving"

Return ONLY a numbered list of topics, one per line."""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=genai_types.Part.from_text(text=prompt)
            )
            
            # Parse topics from response
            topics = []
            for line in response.text.strip().split("\n"):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-") or line.startswith("•")):
                    # Remove numbering/bullets
                    topic = line.lstrip("0123456789.-•* ").strip()
                    if topic:
                        topics.append(topic)
            
            return topics[:7]  # Limit to 7
            
        except Exception as e:
            print(f"⚠️ Error identifying topics: {e}")
            return []
    
    async def _research_topic(self, topic: str) -> str:
        """Research a specific topic using web search."""
        if not self.client:
            return ""
        
        try:
            # Use Gemini with Google Search grounding
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=genai_types.Part.from_text(
                    text=f"""Research and summarize: {topic}

Provide:
1. Key concepts (2-3 sentences)
2. Common mistakes to avoid (2-3 points)
3. Best practice recommendation (1 sentence)

Be concise and practical."""
                ),
                config=genai_types.GenerateContentConfig(
                    tools=[genai_types.Tool(google_search={})]
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️ Error researching {topic}: {e}")
            return ""
    
    async def _identify_best_practices(
        self, 
        goal: str, 
        topics: List[str]
    ) -> Dict[str, List[Dict]]:
        """Identify best practices for the technologies involved."""
        if not self.client:
            return {}
        
        # Extract technologies from topics
        techs = set()
        for topic in topics:
            topic_lower = topic.lower()
            if "flask" in topic_lower:
                techs.add("Flask")
            if "playwright" in topic_lower:
                techs.add("Playwright")
            if "html" in topic_lower:
                techs.add("HTML")
            if "javascript" in topic_lower or "js" in topic_lower:
                techs.add("JavaScript")
            if "css" in topic_lower:
                techs.add("CSS")
        
        best_practices = {}
        
        for tech in techs:
            try:
                prompt = f"""What are 3 critical best practices for {tech} that prevent common errors?

Return as a simple list:
1. Practice: [what to do] | Rationale: [why it matters]
2. Practice: [what to do] | Rationale: [why it matters]
3. Practice: [what to do] | Rationale: [why it matters]"""

                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=genai_types.Part.from_text(text=prompt)
                )
                
                # Parse practices
                practices = []
                for line in response.text.strip().split("\n"):
                    if "|" in line:
                        parts = line.split("|")
                        practice_part = parts[0].split("Practice:")[-1].strip()
                        rationale_part = parts[1].split("Rationale:")[-1].strip()
                        practices.append({
                            "practice": practice_part,
                            "rationale": rationale_part
                        })
                
                if practices:
                    best_practices[tech] = practices
                
            except Exception as e:
                print(f"⚠️ Error getting best practices for {tech}: {e}")
        
        return best_practices
    
    async def _identify_pitfalls(
        self, 
        goal: str, 
        topics: List[str]
    ) -> List[Dict]:
        """Identify common pitfalls and how to avoid them."""
        if not self.client:
            return []
        
        try:
            prompt = f"""For the task "{goal}", what are the 3 most common errors developers make?

For each error, provide:
- Name: Short name for the error pattern
- Description: What goes wrong
- Solution: How to prevent it

Format:
1. Name: [error_name]
   Description: [what goes wrong]
   Solution: [how to prevent]"""

            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=genai_types.Part.from_text(text=prompt),
                config=genai_types.GenerateContentConfig(
                    tools=[genai_types.Tool(google_search={})]
                )
            )
            
            # Parse pitfalls
            pitfalls = []
            current_pitfall = {}
            
            for line in response.text.strip().split("\n"):
                line = line.strip()
                if "Name:" in line:
                    if current_pitfall:
                        pitfalls.append(current_pitfall)
                    current_pitfall = {"name": line.split("Name:")[-1].strip()}
                elif "Description:" in line:
                    current_pitfall["description"] = line.split("Description:")[-1].strip()
                elif "Solution:" in line:
                    current_pitfall["solution"] = line.split("Solution:")[-1].strip()
            
            if current_pitfall:
                pitfalls.append(current_pitfall)
            
            return pitfalls[:3]
            
        except Exception as e:
            print(f"⚠️ Error identifying pitfalls: {e}")
            return []
    
    def get_knowledge_for_execution(self, query: str) -> List[Dict]:
        """
        Get relevant knowledge from the knowledge base for current execution.
        Called during execution to reference learned knowledge.
        """
        return self.kb.search_knowledge(query)


# Example usage
async def test_research():
    """Test the research agent."""
    agent = ResearchAgent()
    
    goal = "Build a friend chat web app with Flask backend and HTML/JS frontend"
    
    research = await agent.research_goal(goal)
    
    print("\n" + "="*70)
    print("📊 RESEARCH RESULTS")
    print("="*70)
    print(f"\nTopics researched: {len(research['topics'])}")
    print(f"Best practices found: {sum(len(p) for p in research['best_practices'].values())}")
    print(f"Pitfalls identified: {len(research['pitfalls'])}")
    

if __name__ == "__main__":
    asyncio.run(test_research())

