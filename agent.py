from google.adk.agents import Agent

from tools import doc_search


root_agent = Agent(
    name="AutonomousResearchAgent",
    model="gemini-2.0-flash",
    description="Autonomous multi-tool agent for private and external research.",
    instruction=(
        "You are an autonomous research assistant. "
        "Use available tools to plan your research, gather private knowledge, "
        "combine it with reasoning, and answer clearly. "
        "Cite retrieved content when appropriate."
    ),
    tools=[
        doc_search,
    ],
)
