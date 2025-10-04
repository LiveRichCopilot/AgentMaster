"""
Web Power Orchestrator
Coordinates comprehensive web research with synthesis
"""

from datetime import datetime
from typing import Dict, Any
from .web_searcher import perform_web_search
from .content_extractor import extract_from_multiple_urls
from vertexai.generative_models import GenerativeModel


def research_topic(query: str, num_sources: int = 5) -> Dict[str, Any]:
    """
    Performs comprehensive web research on a topic.
    
    Workflow:
    1. Search web for relevant URLs
    2. Extract content from each URL
    3. Aggregate all content
    4. Synthesize with Gemini 2.5 Pro
    5. Return formatted answer with citations
    
    Args:
        query: The research question or topic
        num_sources: Number of sources to analyze (default: 5)
        
    Returns:
        Dictionary with:
        - 'query': Original query
        - 'answer': Synthesized answer with citations
        - 'sources': List of sources used
        - 'timestamp': When research was performed
        - 'success': Whether research succeeded
    """
    try:
        print(f"\n🌐 Starting Web Power-Up Research")
        print(f"📋 Query: {query}")
        print(f"🎯 Target sources: {num_sources}")
        print("-" * 60)
        
        # Step 1: Search the web
        print("\n🔍 Step 1: Searching the web...")
        urls = perform_web_search(query, num_results=num_sources)
        
        if not urls:
            return {
                'query': query,
                'answer': "I couldn't find any web results for this query. This might be due to API configuration issues or the query being too specific.",
                'sources': [],
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': 'No search results found'
            }
        
        # Step 2: Extract content from URLs
        print(f"\n📄 Step 2: Extracting content from {len(urls)} URLs...")
        extracted_sources = extract_from_multiple_urls(urls, timeout=10)
        
        if not extracted_sources:
            return {
                'query': query,
                'answer': "I found URLs but couldn't extract content from any of them. The sites might be blocking automated access.",
                'sources': [{'url': url, 'title': 'Failed to extract'} for url in urls],
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': 'No content extracted'
            }
        
        # Step 3: Build context document
        print(f"\n🔄 Step 3: Aggregating content from {len(extracted_sources)} sources...")
        context_parts = []
        for i, source in enumerate(extracted_sources, 1):
            context_parts.append(
                f"===== SOURCE {i} =====\n"
                f"URL: {source['url']}\n"
                f"Title: {source['title']}\n\n"
                f"{source['text']}\n"
            )
        
        context_document = "\n\n".join(context_parts)
        
        # Step 4: Build synthesis prompt
        print(f"\n🧠 Step 4: Synthesizing findings with Gemini 2.5 Pro...")
        
        synthesis_prompt = f"""You are a research assistant performing comprehensive web research.

**User's Question:** {query}

**Your Task:**
I have gathered information from {len(extracted_sources)} web sources. Please:
1. Synthesize the key findings into a comprehensive, well-structured answer
2. Include specific claims, data points, and facts from the sources
3. After each important claim, cite the source using this format: [Source: <number>]
4. If sources contradict each other, note the discrepancy
5. Be thorough but concise - aim for a comprehensive brief, not an essay
6. Structure your answer with clear sections if the topic is complex

**Sources:**
{context_document}

**Provide your synthesized answer with citations:**"""
        
        # Step 5: Call Gemini for synthesis
        try:
            model = GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(
                synthesis_prompt,
                generation_config={
                    'temperature': 0.3,  # Lower temperature for more factual responses
                    'max_output_tokens': 2048
                }
            )
            
            synthesized_answer = response.text
            
        except Exception as e:
            print(f"❌ LLM synthesis error: {e}")
            # Fallback: return the raw content
            synthesized_answer = f"I gathered information but couldn't synthesize it. Here are the key sources:\n\n"
            for i, source in enumerate(extracted_sources, 1):
                synthesized_answer += f"\n{i}. **{source['title']}**\n{source['text'][:500]}...\n"
        
        # Step 6: Format final response
        print(f"\n✅ Research complete!")
        print(f"📊 Sources analyzed: {len(extracted_sources)}")
        print("-" * 60)
        
        # Build sources list
        sources_list = []
        for i, source in enumerate(extracted_sources, 1):
            sources_list.append({
                'number': i,
                'title': source['title'],
                'url': source['url']
            })
        
        return {
            'query': query,
            'answer': synthesized_answer,
            'sources': sources_list,
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'num_sources_analyzed': len(extracted_sources)
        }
        
    except Exception as e:
        print(f"\n❌ Research failed: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'query': query,
            'answer': f"Research failed due to an unexpected error: {str(e)}",
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': str(e)
        }

