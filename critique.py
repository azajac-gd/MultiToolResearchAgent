from google import genai
import os
import json
import logging
from pydantic import BaseModel


client = genai.Client(
    vertexai=os.getenv("USE_VERTEXAI", "False") == "True",
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)

class CritiqueResponse(BaseModel):
    follow_up_questions: list[str]
    stop: bool

def run_critique(query: str, result: str) -> dict:
    model = "gemini-2.0-flash" 
    prompt = f"""
    You are a rigorous research critic. Your role is to determine whether a research result is sufficiently informative, specific, and well-structured to fully answer the user's query.

    Evaluate the following:
    Query: {query}
    Result: {result}

    Your assessment should be based on:
    - Does the result include specific facts, comparisons, or data relevant to the query?
    - Is it free of vague, generic statements (e.g., "it's great", "it improved")?
    - Is the result logically structured and directly answering the key aspects of the query?
    - Are claims supported by reasoning or references?

    Respond only with a JSON object in the format:
    {{
    "follow_up_questions": ["..."],
    "stop": true | false
    }}

    Rules:
    - If the result lacks specificity, depth, or factual content, set "stop": false and suggest 1–3 very precise follow-up questions that would improve the answer.
    - If the result is well-argued and complete, set "stop": true and leave "follow_up_questions" empty.
    - Do NOT include any explanation, reasoning, or commentary outside the JSON object.
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CritiqueResponse,
        },
    )
    text = response.text
    logging.info(f"Critique response: {text}")

    return text if isinstance(text, dict) else json.loads(text)


# result = run_critique("How does the Gemini 2.0 model compare to previous versions in terms of performance and capabilities?",            
#               "Gemini 2.0 is great!"
#           ) 

# print(result)
# if result.get("stop", True):
#     print(result)

# follow_ups = result.get("follow_up_questions", [])
# if not follow_ups:
#     print(result)