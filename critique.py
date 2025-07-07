from google import genai
import os
import json

client = genai.Client(
    vertexai=os.getenv("USE_VERTEXAI", "False") == "True",
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)

def run_critique(query: str, result: str) -> dict:
    model = "gemini-2.0-flash" 
    prompt = f"""
You are an expert research critic. Your task is to evaluate the result of a research agent and decide if further improvement is needed.

Given:
Query: {query}
Result: {result}

Please analyze and return your answer as a JSON object with the following structure:
{{
  "follow_up_questions": [ "..." ],
  "stop": true | false
}}

- If the result is already comprehensive, set "stop": true.
- If not, suggest 1–3 concrete follow-up questions and set "stop": false.
Only return the JSON, nothing else.
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0.2,
        )
    )
    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"stop": True, "follow_up_questions": []}
