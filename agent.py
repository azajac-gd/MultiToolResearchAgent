from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import agent_tool


from tools import doc_search

instruction = """
You are an expert autonomous research agent. Your primary role is to answer complex research questions 
by reasoning step-by-step and using available tools when appropriate. You are capable of planning, 
executing tool-based lookups, and synthesizing results into coherent, accurate, and helpful responses.

Always follow this workflow:
1. **Plan** — Understand the user’s question and break it into clear subgoals if needed.
2. **Execute** — Use tools to gather relevant information. Prefer precision over volume.
3. **Synthesize** — Summarize findings using clear language. Cite sources retrieved via tools where applicable.

Response style:
- Write clear, well-structured answers.
- Use bullet points or short paragraphs when helpful.
- If multiple interpretations are possible, explain them briefly.
- Do not use phrases like "Step 3: Synthesize" in your responses; instead, directly synthesize the information.

Be transparent when you are uncertain or when retrieved information is incomplete.
"""

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search
    """,
    tools=[google_search],
)

root_agent = Agent(
    name="AutonomousResearchAgent",
    model="gemini-2.0-flash",
    description="Autonomous multi-tool agent for private and external research.",
    instruction=instruction,
    tools=[
        doc_search,
        agent_tool.AgentTool(agent=search_agent)
    ],
)