from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

from embedding import GeminiEmbeddings


QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "ifc_report"


vectorstore = Qdrant(
    client=QdrantClient(host="localhost", port=6333),
    collection_name="ifc_report",
    embeddings=GeminiEmbeddings()
)

def retrieve(query):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 50,
        }
    )
    return retriever.get_relevant_documents(query)
