from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from sentence_transformers import CrossEncoder

from services.embedding import GeminiEmbeddings


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



cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, docs: list, top_k: int = 5) -> list:
    pairs = [[query, doc.page_content] for doc in docs]
    scores = cross_encoder.predict(pairs)
    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored_docs[:top_k]]
