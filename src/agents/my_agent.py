from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Optional, List
from langchain.chat_models import init_chat_model
from langfuse import observe
from agents.tools import doc_search, web_search, financial_data, canvas_tool

llm = init_chat_model(model="gemini-2.0-flash")

class State(TypedDict):
    question: str
    plan: Optional[str]
    tool_results: List[str]
    synthesis: Optional[str]
    feedback: Optional[str]
    retry_count: int


@observe
def planner(state: State):
    question = state["question"]
    prompt = f"""
You are a highly skilled research planning agent.

Your job is to break down the following complex research question into a detailed and actionable research plan.

## Requirements:
- Identify 3 to 6 **key sub-questions** that cover all important dimensions of the main question.
- Be comprehensive but not redundant.
- Use a **numbered list** with one clear sub-question per point.
- If needed, include temporal or geographic scopes.

### User Question:
{question}

### Response Format:
1. [Sub-question 1]
2. [Sub-question 2]
...
    """.strip()

    plan = llm.invoke(prompt)
    print(f"🧠 Planner output:\n{plan.content}\n")
    return {"plan": plan.content}


@observe
def executor(state: State):
    llm_with_tools = llm.bind_tools([doc_search, web_search, financial_data])
    plan = state.get("plan", "")

    prompt = f"""
You are a research execution agent.

Your task is to **independently gather raw information** for the following sub-questions using available tools.

## Instructions:
- Use appropriate tools (`doc_search`, `web_search`, `financial_data`) based on each sub-question.
- For each item, briefly mention which tool was used and show raw extracted facts or stats.
- Do **not summarize or explain** findings. Just gather raw results.
- Separate answers clearly.

### Sub-questions to answer:
{plan}

### Response Format:
1. [Sub-question 1]
Tool used: ...
Findings: ...

2. [Sub-question 2]
Tool used: ...
Findings: ...
    """.strip()

    results = llm_with_tools.invoke(prompt)
    print(f"Executor output:\n{results.content}\n")
    return {"tool_results": [results.content]}


@observe
def synthesizer(state: State):
    llm_with_tools = llm.bind_tools([canvas_tool])
    tool_outputs = "\n".join(state["tool_results"])

    prompt = f"""
You are a senior research analyst.

Based on the following raw findings from various tools, write a **clear, well-structured and sourced response** to the original question.

## Guidelines:
- Organize the answer in sections that reflect the key topics/sub-questions.
- Be factual, neutral, and concise.
- Where possible, mention which tool or source produced a specific insight.
- Add a final summary section with overall insights or recommendations.

### Raw Findings:
{tool_outputs}

### Final Answer:
    """.strip()

    synthesis = llm_with_tools.invoke(prompt)
    print(f"Synthesis output:\n{synthesis.content}\n")
    return {"synthesis": synthesis.content}


@observe
def critique(state: State):
    synthesis = state["synthesis"]

    prompt = f"""
You are a critical reviewer.

Read the following synthesis and identify any issues related to:
- Missing sub-topics or dimensions
- Vague or unsupported claims
- Poor structure or lack of flow

## Instructions:
- If the answer is complete and well-structured, say "No major issues."
- If problems exist, describe them briefly and suggest what to improve.

### Synthesis to review:
{synthesis}
    """.strip()

    feedback = llm.invoke(prompt)
    needs_retry = "missing" in feedback.content.lower() or "rewrite" in feedback.content.lower()
    print(f"Critique output:\n{feedback.content}\n")

    return {
        "feedback": feedback.content,
        "retry_count": state["retry_count"] + 1 if needs_retry else state["retry_count"]
    }


def get_research_agent_langgraph(extended_mode: bool = False):
    workflow = StateGraph(State)

    workflow.add_node("planner", planner)
    workflow.add_node("executor", executor)
    workflow.add_node("synthesizer", synthesizer)
    workflow.add_node("critique", critique)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "synthesizer")
    workflow.add_edge("synthesizer", "critique")

    workflow.add_conditional_edges("critique", {
        "planner": lambda state: state["retry_count"] < 3 and (
            "missing" in (state.get("feedback") or "").lower()
            or "rewrite" in (state.get("feedback") or "").lower()
        ),
        END: lambda state: True
    })

    return workflow.compile()
