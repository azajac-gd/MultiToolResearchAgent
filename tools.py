from vectore_store import retrieve

def doc_search(query: str) -> dict:
    chunks = retrieve(query)
    return {"status": "success", "chunks": chunks}
