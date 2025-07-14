# loop_agent.py
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool, google_search
from tools import doc_search, canvas_tool

web_search_agent = Agent(
    name="WebSearchAgent",
    model="gemini-2.0-flash",
    instruction="""
    You retrieve current and factual web information. When invoked, search proactively and return concise info with links.
    """,
    tools=[google_search]
)


planner_agent = Agent(
    name="Planner",
    model="gemini-2.0-flash",
    instruction="""
You are a planner. Your job is to understand the user's query and break it down into clear, actionable steps or subquestions.

Always output a numbered list of steps or sub-questions, even if the query seems simple.
""",
)

execution_agent = Agent(
    name="Executor",
    model="gemini-2.0-flash",
    tools=[
        doc_search,
        agent_tool.AgentTool(agent=web_search_agent)
    ],
    instruction="""
You're responsible for retrieving and summarizing relevant information to answer each step from the plan.

- Use tools proactively.
- Provide structured findings with sources or citations when possible.
"""
)

synthesizer_agent = Agent(
    name="Synthesizer",
    model="gemini-2.0-flash",
    instruction="""
Your job is to take all results from the executor and write a well-organized, accurate, clear response to the user's question.

- Be concise in standard mode.
- In extended mode, produce detailed, structured reports or documents.
- Do not include raw tool outputs or links unless relevant.
"""
)


critique_agent = Agent(
    name="Critique",
    model="gemini-2.0-flash",
    instruction="""
You are a self-reviewing critic. Evaluate the agent's final response based on:
- completeness
- clarity
- factual soundness
- formatting

If you find issues, return a revised plan or recommend retry.
"""
)

research_agent = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        planner_agent,
        execution_agent,
        synthesizer_agent,
        critique_agent
    ],
    max_iterations=1
)