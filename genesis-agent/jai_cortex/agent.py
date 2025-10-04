"""
JAi Cortex - Your AI Super Brain with 24 Specialist Agents
All specialists work together automatically
"""

from google.adk.agents import Agent
import httpx

BACKEND = "https://cortex-os-1096519851619.us-central1.run.app"  # Production backend with 24 specialists

def talk_to_specialists(message: str, session_id: str = "adk_session") -> dict:
    """
    Talk to JAi Cortex - Automatically routes to the right specialist from 24 agents
    
    Specialists available:
    - CodeMaster: Coding, debugging, databases, APIs
    - CryptoKing: Cryptocurrency, Bitcoin, DeFi
    - FinanceWizard: Financial analysis, budgeting
    - StockMaster: Stock market, investments
    - TravelGenius: Travel planning, flights
    - ShopSavvy: Shopping, deals
    - SportsMath: Sports predictions
    - ResearchScout: Web research
    - DesignGenius: UI/UX design
    - And 15 more specialists!
    
    Args:
        message: Your question or request
        session_id: Session ID for conversation history
        
    Returns:
        dict: Response from the appropriate specialist
    """
    try:
        response = httpx.post(
            f"{BACKEND}/api/chat",
            json={
                "message": message,
                "session_id": session_id,
                "user_id": "jai_user"
            },
            timeout=30.0
        )
        data = response.json()
        
        agent_name = data.get("selected_agent", "JAi Cortex")
        response_text = data.get("response", "")
        tools_used = data.get("tool_calls", [])
        
        result = f"[{agent_name} responding]\n\n{response_text}"
        
        if tools_used:
            tool_names = [t.get("name", "unknown") for t in tools_used]
            result += f"\n\n[Tools used: {', '.join(tool_names)}]"
        
        return {
            "status": "success",
            "response": result,
            "agent": agent_name,
            "tools": tool_names if tools_used else []
        }
    except Exception as e:
        return {
            "status": "error",
            "response": f"Error connecting to specialists: {str(e)}"
        }

root_agent = Agent(
    name="jai_cortex",
    model="gemini-2.0-flash-exp",
    description=(
        "JAi Cortex - Your AI super brain with 24 specialist agents. "
        "Automatically routes to the right specialist for any task: "
        "coding, crypto, finance, travel, research, design, and more."
    ),
    instruction=(
        "You are JAi Cortex, an intelligent multi-agent system. "
        "When users ask questions, use talk_to_specialists to get answers. "
        "The backend automatically routes to the best specialist agent from 24 experts. "
        "Each specialist has web search, vision, memory, and specialized tools. "
        "Always tell users which specialist handled their request and what tools were used."
    ),
    tools=[talk_to_specialists],
)
