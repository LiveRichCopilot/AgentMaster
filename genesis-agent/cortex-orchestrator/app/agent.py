"""
Cortex Orchestrator - Per software-bug-assistant/tools.py lines 43-52 (uses Agent with AgentTool)
"""
from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search

# 23 sub-agents using Agent (not LlmAgent) per working example
codemaster = Agent(name="CodeMaster", model="gemini-2.5-flash", instruction="Help with code, bugs, APIs, databases")
cloud_expert = Agent(name="CloudExpert", model="gemini-2.5-flash", instruction="Help with GCP services")
database_expert = Agent(name="DatabaseExpert", model="gemini-2.5-flash", instruction="Help with databases")
automation_wizard = Agent(name="AutomationWizard", model="gemini-2.5-flash", instruction="Help with automation")
api_integrator = Agent(name="ApiIntegrator", model="gemini-2.5-flash", instruction="Help with APIs")
web_searcher = Agent(name="WebSearcher", model="gemini-2.5-flash", instruction="Help with research", tools=[google_search])
media_processor = Agent(name="MediaProcessor", model="gemini-2.5-flash", instruction="Help with media")
vision_analyzer = Agent(name="VisionAnalyzer", model="gemini-2.5-flash", instruction="Help with images")
document_parser = Agent(name="DocumentParser", model="gemini-2.5-flash", instruction="Help with documents")
file_manager = Agent(name="FileManager", model="gemini-2.5-flash", instruction="Help with files")
workspace_manager = Agent(name="WorkspaceManager", model="gemini-2.5-flash", instruction="Help with Workspace")
data_processor = Agent(name="DataProcessor", model="gemini-2.5-flash", instruction="Help with data")
notebook_scientist = Agent(name="NotebookScientist", model="gemini-2.5-flash", instruction="Help with data science")
knowledge_base = Agent(name="KnowledgeBase", model="gemini-2.5-flash", instruction="Help with knowledge")
security_guard = Agent(name="SecurityGuard", model="gemini-2.5-flash", instruction="Help with security")
performance_monitor = Agent(name="PerformanceMonitor", model="gemini-2.5-flash", instruction="Help with monitoring")
error_handler = Agent(name="ErrorHandler", model="gemini-2.5-flash", instruction="Help with debugging")
calendar_manager = Agent(name="CalendarManager", model="gemini-2.5-flash", instruction="Help with calendar")
email_manager = Agent(name="EmailManager", model="gemini-2.5-flash", instruction="Help with email")
backup_manager = Agent(name="BackupManager", model="gemini-2.5-flash", instruction="Help with backups")
version_controller = Agent(name="VersionController", model="gemini-2.5-flash", instruction="Help with Git")
note_keeper = Agent(name="NoteKeeper", model="gemini-2.5-flash", instruction="Help with notes")
personal_assistant = Agent(name="PersonalAssistant", model="gemini-2.5-flash", instruction="Help with tasks")

# Root orchestrator using Agent (per working example)
root_agent = Agent(
    name="cortex_orchestrator",
    model="gemini-2.5-flash",
    instruction="You are Cortex OS coordinating 23 specialists. Delegate to the right specialist tool based on the user request.",
    tools=[
        AgentTool(agent=codemaster), AgentTool(agent=cloud_expert), AgentTool(agent=database_expert),
        AgentTool(agent=automation_wizard), AgentTool(agent=api_integrator), AgentTool(agent=web_searcher),
        AgentTool(agent=media_processor), AgentTool(agent=vision_analyzer), AgentTool(agent=document_parser),
        AgentTool(agent=file_manager), AgentTool(agent=workspace_manager), AgentTool(agent=data_processor),
        AgentTool(agent=notebook_scientist), AgentTool(agent=knowledge_base), AgentTool(agent=security_guard),
        AgentTool(agent=performance_monitor), AgentTool(agent=error_handler), AgentTool(agent=calendar_manager),
        AgentTool(agent=email_manager), AgentTool(agent=backup_manager), AgentTool(agent=version_controller),
        AgentTool(agent=note_keeper), AgentTool(agent=personal_assistant),
    ],
)
