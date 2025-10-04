# Web Power-Up Implementation Specification
## Perplexity-like System for JAi Cortex OS

**Goal:** Enable JAi to perform comprehensive web research with synthesis and citation, similar to Perplexity AI.

---

## Architecture Overview

```
User Query
    ↓
Orchestrator (main_agent.py)
    ↓
Web Searcher (web_searcher.py) → [Gets 5-10 URLs]
    ↓
Content Extractor (content_extractor.py) → [Extracts clean text from each URL]
    ↓
Aggregator → [Combines all text into context document]
    ↓
Synthesizer (Gemini 2.5 Pro) → [Generates answer with citations]
    ↓
Formatted Response with Sources
```

---

## Module Specifications

### 1. Web Searcher (`web_searcher.py`)

**Purpose:** Query search engines and return relevant URLs

**Dependencies:**
```bash
pip install requests
```

**API Requirements:**
- Google Custom Search API Key
- Custom Search Engine ID

**Function Signature:**
```python
def perform_web_search(query: str, num_results: int = 5) -> List[str]:
    """
    Performs web search and returns list of URLs
    
    Args:
        query: User's search query
        num_results: Number of results to return (default: 5)
        
    Returns:
        List of URL strings
    """
```

**Environment Variables:**
```bash
GOOGLE_SEARCH_API_KEY=your_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here
```

**Implementation Notes:**
- Use Google Custom Search JSON API
- Handle rate limiting (100 queries/day free, then $5 per 1000)
- Include error handling for API failures
- Return empty list on error, don't crash

---

### 2. Content Extractor (`content_extractor.py`)

**Purpose:** Fetch and extract clean text from webpages

**Dependencies:**
```bash
pip install requests beautifulsoup4 trafilatura
```

**Function Signature:**
```python
def extract_text_from_url(url: str, timeout: int = 10) -> Dict[str, str]:
    """
    Fetches URL and extracts main text content
    
    Args:
        url: URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with:
        - 'url': Original URL
        - 'title': Page title
        - 'text': Extracted content
        - 'error': Error message if failed
    """
```

**Implementation Strategy:**
1. **Primary:** Use `trafilatura` (better article extraction)
2. **Fallback:** Use `BeautifulSoup4` if trafilatura fails
3. **Timeout:** 10 seconds per URL to avoid hanging
4. **Cleaning:** Remove scripts, styles, navigation, ads
5. **Length Limit:** Cap at 5000 words per article to stay within token limits

**Code Pattern:**
```python
import trafilatura
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str, timeout: int = 10) -> Dict[str, str]:
    try:
        # Fetch page
        response = requests.get(url, timeout=timeout, headers={'User-Agent': 'JAi-Research-Bot/1.0'})
        response.raise_for_status()
        
        # Try trafilatura first (better article extraction)
        text = trafilatura.extract(response.content, include_comments=False, include_tables=False)
        
        if not text:
            # Fallback to BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            text = soup.get_text(separator='\\n', strip=True)
        
        # Get title
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').string if soup.find('title') else 'Untitled'
        
        return {
            'url': url,
            'title': title,
            'text': text[:5000],  # Limit length
            'error': None
        }
        
    except Exception as e:
        return {
            'url': url,
            'title': None,
            'text': '',
            'error': str(e)
        }
```

---

### 3. Web Power Orchestrator (`web_power_orchestrator.py`)

**Purpose:** Coordinate the entire research workflow

**Function Signature:**
```python
def research_topic(query: str, num_sources: int = 5) -> Dict[str, Any]:
    """
    Performs comprehensive web research on a topic
    
    Workflow:
    1. Search web for relevant URLs
    2. Extract content from each URL
    3. Aggregate content
    4. Synthesize with LLM
    5. Return formatted answer with citations
    
    Args:
        query: User's research question
        num_sources: Number of sources to use (default: 5)
        
    Returns:
        Dictionary with:
        - 'query': Original query
        - 'answer': Synthesized answer
        - 'sources': List of sources used with URLs
        - 'timestamp': When research was performed
    """
```

**Workflow Steps:**
```python
def research_topic(query: str, num_sources: int = 5) -> Dict[str, Any]:
    # Step 1: Search
    urls = perform_web_search(query, num_results=num_sources)
    
    # Step 2: Extract content from each URL
    sources = []
    for url in urls:
        content = extract_text_from_url(url)
        if content['text']:  # Only include if we got content
            sources.append(content)
    
    # Step 3: Build context document
    context = "\\n\\n---SOURCE---\\n\\n".join([
        f"URL: {s['url']}\\nTitle: {s['title']}\\n\\n{s['text']}"
        for s in sources
    ])
    
    # Step 4: Build synthesis prompt
    synthesis_prompt = f"""You are a research assistant. A user asked: "{query}"

I have gathered information from {len(sources)} web sources. Please:
1. Synthesize the key findings into a comprehensive, well-structured answer
2. Include specific claims and data points
3. Cite sources using [Source: URL] format after each claim
4. If sources contradict each other, note the discrepancy
5. Be thorough but concise

Sources:
{context}

Provide your synthesized answer:"""
    
    # Step 5: Call LLM for synthesis
    from vertexai.generative_models import GenerativeModel
    model = GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(synthesis_prompt)
    
    # Step 6: Format response
    return {
        'query': query,
        'answer': response.text,
        'sources': [{'title': s['title'], 'url': s['url']} for s in sources],
        'timestamp': datetime.now().isoformat()
    }
```

---

### 4. JAi Integration (`jai_cortex/agent.py`)

**Add as new tool:**

```python
def advanced_web_research(query: str, num_sources: int = 5, tool_context: ToolContext = None) -> dict:
    """Perform comprehensive web research on a topic with synthesis and citations.
    
    This is JAi's "Perplexity mode" - it searches the web, reads multiple sources,
    and synthesizes findings into a comprehensive answer with citations.
    
    Use this when:
    - User asks for in-depth research on a topic
    - User wants multiple sources analyzed
    - User asks "research X and give me a comprehensive brief"
    - User wants cited information
    
    Args:
        query: The research question or topic
        num_sources: Number of web sources to analyze (default: 5)
        
    Returns:
        dict: Synthesized answer with citations and source list
    """
    try:
        from .web_power_orchestrator import research_topic
        
        result = research_topic(query, num_sources=num_sources)
        
        return {
            'status': 'success',
            'query': result['query'],
            'answer': result['answer'],
            'sources': result['sources'],
            'num_sources_analyzed': len(result['sources'])
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Web research failed: {str(e)}'
        }
```

**Update JAi's instruction:**
```
10. **advanced_web_research** - Comprehensive web research with synthesis and citations (Perplexity-style)
```

---

## Setup Instructions for Developer

### Step 1: Get API Keys

**Google Custom Search:**
1. Go to: https://console.cloud.google.com/
2. Enable "Custom Search API"
3. Create credentials → API Key
4. Go to: https://programmablesearchengine.google.com/
5. Create a new search engine
6. Get your Search Engine ID

**Set environment variables:**
```bash
export GOOGLE_SEARCH_API_KEY="your_api_key"
export GOOGLE_SEARCH_ENGINE_ID="your_engine_id"
```

### Step 2: Install Dependencies

```bash
cd genesis-agent/agent_backend
pip install requests beautifulsoup4 trafilatura
```

### Step 3: Create Files

```bash
cd jai_cortex
touch web_searcher.py
touch content_extractor.py
touch web_power_orchestrator.py
```

### Step 4: Implement Each Module

Copy the code patterns from this spec into each file.

### Step 5: Test Modules Independently

**Test web searcher:**
```python
from jai_cortex.web_searcher import perform_web_search
urls = perform_web_search("quantum computing breakthroughs 2025")
print(urls)
```

**Test content extractor:**
```python
from jai_cortex.content_extractor import extract_text_from_url
content = extract_text_from_url(urls[0])
print(content['title'], content['text'][:200])
```

**Test orchestrator:**
```python
from jai_cortex.web_power_orchestrator import research_topic
result = research_topic("What are the latest quantum computing breakthroughs?")
print(result['answer'])
```

### Step 6: Integrate with JAi

1. Add `advanced_web_research()` function to `agent.py`
2. Add `FunctionTool(advanced_web_research)` to tools list
3. Update instruction to mention the new capability
4. Restart ADK server

---

## Expected Usage

**User asks JAi:**
```
"Research the latest developments in AI safety and give me a comprehensive brief with sources"
```

**JAi responds:**
```
I'll conduct comprehensive research on AI safety developments for you.

[Uses advanced_web_research tool]

**AI Safety: Latest Developments (2025)**

Recent developments in AI safety have focused on three key areas:

1. **Constitutional AI and Alignment**: 
Research teams have made significant progress in training models with built-in 
safety constraints... [Source: https://anthropic.com/research/constitutional-ai]

2. **Interpretability and Transparency**:
New techniques for understanding model decision-making have emerged, including...
[Source: https://openai.com/research/interpretability]

3. **Red-Teaming and Adversarial Testing**:
Organizations are now employing systematic adversarial testing...
[Source: https://deepmind.google/safety/]

**Sources:**
1. Anthropic - Constitutional AI Research
2. OpenAI - Interpretability Research
3. DeepMind - AI Safety Approaches
```

---

## Performance Considerations

**Speed:**
- Each URL fetch: ~1-3 seconds
- Total for 5 sources: ~5-15 seconds
- LLM synthesis: ~5-10 seconds
- **Total time: 10-25 seconds** (acceptable for comprehensive research)

**Costs:**
- Google Search API: $5 per 1000 queries (or 100/day free)
- Gemini API: Already covered
- **Total: ~$0.005 per research query**

**Token Usage:**
- Each source: ~1000-2000 tokens
- 5 sources + prompt: ~7000-12000 tokens input
- Response: ~1000-2000 tokens output
- **Total: ~10,000-15,000 tokens per query**

---

## Testing Checklist

- [ ] Web searcher returns valid URLs
- [ ] Content extractor handles normal articles
- [ ] Content extractor handles paywalls gracefully (returns error)
- [ ] Content extractor handles 404s gracefully
- [ ] Orchestrator handles partial failures (some URLs fail)
- [ ] Synthesis includes proper citations
- [ ] Integration with JAi works end-to-end
- [ ] Error messages are helpful
- [ ] Performance is acceptable (< 30 seconds)

---

## Future Enhancements

**Phase 2 (Optional):**
- Add PDF extraction capability
- Add image analysis from search results
- Add real-time data (stock prices, weather)
- Add multi-language support
- Add fact-checking against known sources

**Phase 3 (Optional):**
- Build a caching layer (don't re-scrape same URLs)
- Add source quality scoring
- Add citation verification
- Create a dedicated WebResearcher sub-agent

---

## Files to Create

```
jai_cortex/
├── web_searcher.py          (NEW - 50 lines)
├── content_extractor.py     (NEW - 80 lines)
├── web_power_orchestrator.py (NEW - 100 lines)
└── agent.py                 (MODIFY - add advanced_web_research tool)
```

**Total new code: ~250 lines**
**Estimated implementation time: 1-2 days**

---

## Questions for Code Master?

If your developer has questions while implementing, they can ask:
- "How do I handle rate limiting for the Search API?"
- "What's the best way to handle JavaScript-heavy sites?"
- "Should I cache scraped content?"

CodeMaster will provide specific technical guidance!

