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

from pydantic import BaseModel
from typing import List
import json
import logging

from pydantic import BaseModel
import json
import logging

class CritiqueResponseWithFeedback(BaseModel):
    critique: str 
    score: int 

def run_critique(query: str, result: str) -> dict:
    model = "gemini-2.0-flash"
    prompt = f"""
You are a rigorous research critic. Your job is to evaluate the quality of the result provided in response to a user's query.

Evaluate:
Query: {query}
Result: {result}

Assess the result based on:
- Does it include specific facts, comparisons, or data relevant to the query?
- Is it free of vague, generic statements (e.g., "it's great", "it improved")?
- Is the result logically structured and clearly answers the key aspects of the query?
- Are claims supported by reasoning, evidence, or references?

Respond only with a JSON object in the format:
{{
  "critique": "Write a clear, constructive critique of what is missing, vague, incorrect, or could be improved in the result.",
  "score": 0-10  // from 0 (poor answer) to 10 (excellent, complete answer)
}}

Rules:
- Be specific in your critique (e.g., missing data, vague phrasing, logical leaps).
- If the result is fully correct and complete, return "stop": true and "score": 10, with an empty string in "critique".
- Do NOT include any explanation or commentary outside the JSON object.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CritiqueResponseWithFeedback,
        },
    )
    text = response.text
    logging.info(f"Critique response: {text}")

    return text if isinstance(text, dict) else json.loads(text)




# result = run_critique("What is the apple?",   
#                       "Apple is a fruit that is red or green and grows on trees. It is sweet and can be eaten raw or used in cooking."         
#           ) 

# print(result)