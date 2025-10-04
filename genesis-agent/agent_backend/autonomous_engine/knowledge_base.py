"""
Continuous Learning Knowledge Base
Stores and retrieves knowledge learned from web research and experience.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class KnowledgeBase:
    """
    Persistent knowledge storage that grows over time.
    
    The agent learns about topics, stores that knowledge,
    and references it for future tasks.
    """
    
    def __init__(self, storage_path: str = None):
        """Initialize knowledge base with persistent storage."""
        if storage_path is None:
            storage_path = Path(__file__).parent / "knowledge_base.json"
        
        self.storage_path = Path(storage_path)
        self.knowledge = self._load()
    
    def _load(self) -> Dict:
        """Load knowledge from persistent storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load knowledge base: {e}")
                return self._init_knowledge()
        return self._init_knowledge()
    
    def _init_knowledge(self) -> Dict:
        """Initialize empty knowledge structure."""
        return {
            "topics": {},  # Topic-based knowledge
            "patterns": {},  # Error patterns and solutions
            "best_practices": {},  # Coding best practices
            "tools": {},  # Tool-specific knowledge
            "statistics": {
                "total_topics": 0,
                "total_updates": 0,
                "last_updated": None
            }
        }
    
    def _save(self):
        """Persist knowledge to disk."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save knowledge base: {e}")
    
    def add_topic_knowledge(
        self, 
        topic: str, 
        knowledge: str, 
        source: str = "research"
    ):
        """
        Add knowledge about a topic.
        
        Args:
            topic: The topic (e.g., "Flask routing", "Playwright selectors")
            knowledge: What was learned
            source: Where it came from (research, experience, error)
        """
        if topic not in self.knowledge["topics"]:
            self.knowledge["topics"][topic] = {
                "entries": [],
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "update_count": 0
            }
        
        # Add new entry
        self.knowledge["topics"][topic]["entries"].append({
            "knowledge": knowledge,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update metadata
        self.knowledge["topics"][topic]["updated"] = datetime.now().isoformat()
        self.knowledge["topics"][topic]["update_count"] += 1
        self.knowledge["statistics"]["total_updates"] += 1
        self.knowledge["statistics"]["last_updated"] = datetime.now().isoformat()
        
        if len(self.knowledge["topics"][topic]["entries"]) == 1:
            self.knowledge["statistics"]["total_topics"] += 1
        
        self._save()
        print(f"📚 LEARNED: Added knowledge about '{topic}' (source: {source})")
    
    def get_topic_knowledge(self, topic: str) -> Optional[List[Dict]]:
        """Retrieve all knowledge about a topic."""
        if topic in self.knowledge["topics"]:
            return self.knowledge["topics"][topic]["entries"]
        return None
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """
        Search knowledge base for relevant information.
        
        Returns list of matching entries with topic and content.
        """
        results = []
        query_lower = query.lower()
        
        for topic, data in self.knowledge["topics"].items():
            # Check if query matches topic
            if query_lower in topic.lower():
                results.append({
                    "topic": topic,
                    "relevance": "topic_match",
                    "entries": data["entries"]
                })
            else:
                # Check if query matches any knowledge entry
                for entry in data["entries"]:
                    if query_lower in entry["knowledge"].lower():
                        results.append({
                            "topic": topic,
                            "relevance": "content_match",
                            "entry": entry
                        })
        
        return results
    
    def add_pattern(
        self, 
        pattern_name: str, 
        description: str, 
        solution: str
    ):
        """
        Store a reusable pattern (error pattern, design pattern, etc.).
        """
        self.knowledge["patterns"][pattern_name] = {
            "description": description,
            "solution": solution,
            "timestamp": datetime.now().isoformat(),
            "use_count": 0
        }
        self._save()
        print(f"📚 LEARNED: Stored pattern '{pattern_name}'")
    
    def get_pattern(self, pattern_name: str) -> Optional[Dict]:
        """Retrieve a stored pattern."""
        pattern = self.knowledge["patterns"].get(pattern_name)
        if pattern:
            pattern["use_count"] += 1
            self._save()
        return pattern
    
    def add_best_practice(
        self, 
        technology: str, 
        practice: str, 
        rationale: str
    ):
        """Store best practices for technologies."""
        if technology not in self.knowledge["best_practices"]:
            self.knowledge["best_practices"][technology] = []
        
        self.knowledge["best_practices"][technology].append({
            "practice": practice,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
        print(f"📚 LEARNED: Best practice for {technology}")
    
    def get_best_practices(self, technology: str) -> List[Dict]:
        """Get all best practices for a technology."""
        return self.knowledge["best_practices"].get(technology, [])
    
    def add_tool_knowledge(
        self, 
        tool_name: str, 
        usage: str, 
        tips: List[str]
    ):
        """Store knowledge about how to use a tool."""
        self.knowledge["tools"][tool_name] = {
            "usage": usage,
            "tips": tips,
            "timestamp": datetime.now().isoformat()
        }
        self._save()
        print(f"📚 LEARNED: How to use {tool_name}")
    
    def get_tool_knowledge(self, tool_name: str) -> Optional[Dict]:
        """Get knowledge about a tool."""
        return self.knowledge["tools"].get(tool_name)
    
    def get_summary(self) -> Dict:
        """Get a summary of what's stored in the knowledge base."""
        return {
            "total_topics": len(self.knowledge["topics"]),
            "total_patterns": len(self.knowledge["patterns"]),
            "total_best_practices": sum(
                len(practices) 
                for practices in self.knowledge["best_practices"].values()
            ),
            "total_tools": len(self.knowledge["tools"]),
            "statistics": self.knowledge["statistics"]
        }
    
    def print_summary(self):
        """Print a human-readable summary."""
        summary = self.get_summary()
        print("\n" + "="*60)
        print("📚 KNOWLEDGE BASE SUMMARY")
        print("="*60)
        print(f"Topics learned: {summary['total_topics']}")
        print(f"Patterns stored: {summary['total_patterns']}")
        print(f"Best practices: {summary['total_best_practices']}")
        print(f"Tools documented: {summary['total_tools']}")
        print(f"Total updates: {summary['statistics']['total_updates']}")
        print(f"Last updated: {summary['statistics']['last_updated']}")
        print("="*60 + "\n")


# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase()
    
    # Add some example knowledge
    kb.add_topic_knowledge(
        topic="Flask routing",
        knowledge="Flask uses @app.route() decorator. The route must have a return value.",
        source="research"
    )
    
    kb.add_topic_knowledge(
        topic="Playwright selectors",
        knowledge="Playwright uses CSS selectors by default. Use #id for IDs, .class for classes.",
        source="web_search"
    )
    
    kb.add_pattern(
        pattern_name="missing_ui_elements",
        description="When Playwright can't find UI elements in HTML",
        solution="Ensure HTML has the exact selector IDs. Use proven template if necessary."
    )
    
    kb.print_summary()
    
    # Search knowledge
    results = kb.search_knowledge("selector")
    print(f"\nSearch results for 'selector': {len(results)} matches")
    for result in results:
        print(f"  - {result['topic']}")

