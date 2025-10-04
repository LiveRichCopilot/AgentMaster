# ADK Tools API Reference

Based on documentation research, here's how to properly define and use tools in ADK agents.

## 1. Built-in Tools

**Available built-in tools:**
- `google_search` - Google Search grounding
- `BuiltInCodeExecutor` - Sandboxed code execution
- `VertexAiSearchTool` - Private Vertex AI Search
- `BigQueryToolset` - BigQuery interactions

**Usage:**
```python
from google.adk.tools import google_search
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.5-pro",
    name="my_agent",
    instruction="...",
    tools=[google_search],  # Use directly
)
```

## 2. Custom Function Tools

**Requirements:**
- Must have type hints on ALL parameters
- Must have `tool_context: ToolContext` as LAST parameter
- Must return `dict` or `str`
- Must have a descriptive docstring
- NO DEFAULT VALUES on parameters

**Example:**
```python
from google.adk.tools import ToolContext

def my_custom_tool(param1: str, param2: int, tool_context: ToolContext) -> dict:
    """Describe what this tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        dict: Contains the result
    ```
    # Your implementation
    return {"status": "success", "result": "..."}
```

**Usage - Two ways:**
```python
# Method 1: Direct (ADK auto-wraps)
tools=[my_custom_tool]

# Method 2: Explicit wrapper
from google.adk.tools import FunctionTool
tools=[FunctionTool(func=my_custom_tool)]
```

## 3. AgentTool (Call other agents as tools)

**Pattern:**
```python
from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search

# Create a specialist agent
search_specialist = Agent(
    model="gemini-2.5-flash",
    name="search_specialist",
    instruction="You're a search specialist",
    tools=[google_search],
)

# Wrap it as a tool
search_tool = AgentTool(search_specialist)

# Use in main agent
main_agent = Agent(
    model="gemini-2.5-pro",
    name="main_agent",
    instruction="...",
    tools=[search_tool],  # Use the wrapped agent
)
```

## 4. Combining Multiple Tools

```python
tools=[
    google_search,                      # Built-in
    FunctionTool(func=my_function),     # Custom function
    agent_tool,                          # Another agent
]
```

## 5. Calling Deployed Vertex AI Agents

**Pattern for calling deployed reasoning engines:**
```python
import requests
from google.adk.tools import ToolContext

def call_deployed_agent(task: str, agent_endpoint: str, tool_context: ToolContext) -> dict:
    """Call a deployed Vertex AI agent.
    
    Args:
        task: The task to send to the agent
        agent_endpoint: Vertex AI agent endpoint URL
        
    Returns:
        dict: Response from the agent
    ```
    response = requests.post(
        agent_endpoint,
        json={"query": task},
        headers={"Content-Type": "application/json"}
    )
    return response.json()
```

## 6. Important Notes

- **Warning**: An agent can only use ONE type of built-in tool at a time
- Built-in tools cannot be used in sub-agents
- Functions can be `async` if they need to be
- Return type MUST be `dict` or `str` (JSON-serializable)
- Docstrings are CRITICAL - they tell the LLM when/how to use the tool

## 7. Testing Pattern

**Start small and add incrementally:**
1. Start with just `google_search`
2. Add one custom function
3. Test it works
4. Add more tools one by one
5. Test after each addition

This prevents debugging 20+ tools at once!

