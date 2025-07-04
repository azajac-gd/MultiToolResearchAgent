from vectore_store import retrieve


def doc_search(query: str) -> dict:
    """
    Search internal document "IFC Annual Report 2024 financials" semantically for relevant content.

    Args:
        query (str): What the user is looking for.

    Returns:
        dict: List of chunks and status.
    """
    chunks = retrieve(query)
    return {"status": "success", "chunks": chunks}


