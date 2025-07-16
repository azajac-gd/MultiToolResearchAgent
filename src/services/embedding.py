import os
from google import genai
from langchain.embeddings.base import Embeddings
from langfuse import observe
from google.genai import types


client = genai.Client(
    vertexai=os.getenv("USE_VERTEXAI", "False") == "True",
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)


class GeminiEmbeddings(Embeddings):
    def __init__(self, client=client, model: str = "text-embedding-004"):
        self.client = client
        self.model = model

    @observe()
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        batch_size = 16
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            responses = [
                self.client.models.embed_content(
                    model=self.model,
                    contents={"parts": [{"text": text}]},
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
                )
                for text in batch
            ]
            embeddings.extend([r.embeddings[0].values for r in responses])
        return embeddings
    
    @observe()
    def embed_query(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model,
            contents={"parts": [{"text": text}]},
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        return response.embeddings[0].values