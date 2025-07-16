from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool, google_search
from agents.tools import doc_search, canvas_tool, exit_loop, financial_data
from langfuse import observe
from agents.config_loader import load_agent_config

@observe
def get_research_agent(extended_mode: bool = False):
    cfg = load_agent_config()

    planner_instruction = cfg["long_planner"] if extended_mode else cfg["short_planner"]
    synthesizer_instruction = cfg["long_synthesizer"] if extended_mode else cfg["short_synthesizer"]
    execution_instruction = cfg["execution_instruction"]
    critique_instruction = cfg["critique_instruction"]
    web_search_instruction = cfg["web_search_instruction"]

    gemini_model = "gemini-2.0-flash"

    web_search_agent = Agent(
        name="WebSearchAgent",
        model=gemini_model,
        instruction=web_search_instruction,
        tools=[google_search]
    )

    planner_agent = Agent(
        name="Planner",
        model=gemini_model,
        instruction=planner_instruction
    )

    execution_agent = Agent(
        name="Executor",
        model=gemini_model,
        tools=[
            doc_search,
            agent_tool.AgentTool(agent=web_search_agent, skip_summarization=True),
            financial_data
        ],
        instruction=execution_instruction
    )

    synthesizer_agent = Agent(
        name="Synthesizer",
        model="gemini-2.5-flash",
        instruction=synthesizer_instruction,
        tools=[canvas_tool]
    )

    critique_agent = Agent(
        name="Critique",
        model=gemini_model,
        instruction=critique_instruction,
        tools=[exit_loop]
    )

    return LoopAgent(
        name="ResearchAgent",
        sub_agents=[
            planner_agent,
            execution_agent,
            synthesizer_agent,
            critique_agent
        ],
        max_iterations=3
    )
