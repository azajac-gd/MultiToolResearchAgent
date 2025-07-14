import logging

from pydantic import BaseModel
from jinja2 import Template, TemplateError

from vectore_store import retrieve, rerank


def doc_search(query: str) -> dict:
    """
    Search internal document "IFC Annual Report 2024 financials" semantically for relevant content.

    Args:
        query (str): What the user is looking for.

    Returns:
        dict: List of chunks and status.
    """
    retrieved = retrieve(query)
    chunks = rerank(query, retrieved)
    return {"status": "success", "chunks": chunks}


class CanvasInput(BaseModel):
    content_type: str
    data: dict
    template: str


def canvas_tool(input: dict) -> str:
    """
    Generate structured outputs like reports, docs or code using Jinja2 templates. Use this tool when the user expects a specific format or wants a long-form answer.

    Args:
        input (CanvasInput): Input data containing content type, data, and template.

    Returns:
        str: Rendered output from the Jinja2 template.
    """
    canvas_input = CanvasInput(**input)
    try:
        tmpl = Template(canvas_input.template)
        rendered = tmpl.render(**canvas_input.data)
        logging.info(f"Rendered {canvas_input.content_type} output successfully.")
        return rendered
    except TemplateError as e:
        logging.error(f"Jinja2 template rendering failed: {str(e)}")
        return (
            f"[CanvasTool Error] Failed to render the {canvas_input.content_type} output due to template error: {str(e)}"
        )



