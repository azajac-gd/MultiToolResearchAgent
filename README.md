# Multi-Tool Research Agent

A conversational research assistant powered by **Google Vertex AI's Reasoning Engine (`AdkApp`)** and a **Streamlit UI**.  
Supports extended mode for synthesizing long-form reports.  
Designed to run locally with GCP Application Default Credentials (ADC).

---

## Architecture
[User] ⇄ [Streamlit Frontend UI] ⇄ [ADK Reasoning Engine (AdkApp)]
⇓
[Tool Integration: Web Search, Doc Search, Canvas Editor, Financial Tools]
⇓
[Vertex AI (Gemini Models via genai SDK)]

---

- **Planner–Executor–Synthesizer Loop Agent** using `google.generativeai.agent.AdkApp`
- Tools include: web search, vector-based doc search, table/chart generation
- Built-in critique & retry logic
- Session memory with chat history & report persistence

---

## Features

- Vertex AI Gemini via Reasoning Engine (ADK)
- Conversational UI with Streamlit
- Loop agent with planning, execution, synthesis
- Extended mode for long-form report generation

---

## Requirements

- Python **3.10+**
- Google Cloud project with **Vertex AI API** enabled
- `gcloud` CLI installed and authenticated (`gcloud auth application-default login`)

---

## Installation (Local, no Docker)

1. **Clone the repository**

    ```bash
    git clone https://github.com/azajac-gd/MultiToolResearchAgent.git
    cd MultiToolResearchAgent
    ```

2. **Create and activate virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Python dependencies**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Authenticate with Google Cloud**

    Make sure you're logged into an account that has access to Vertex AI:

    ```bash
    gcloud auth application-default login
    ```

    This will generate a local ADC file (usually under `~/.config/gcloud/application_default_credentials.json`).

5. **Set environment variables**

    You can create a `.env` file or set them manually:

    ```env
    PROJECT_ID=your-project-id
    LOCATION=us-central1
    USE_VERTEXAI=True
    ```

6. **Run the Streamlit app**

    ```bash
    streamlit run src/app.py
    ```

---

## Troubleshooting

- **Vertex AI authentication errors**  
  → Ensure you ran `gcloud auth application-default login` and that your user has sufficient IAM roles.

- **Missing location/project errors**  
  → Double-check your environment variables or pass them in directly to `genai.Client(...)`.

- **Module errors (e.g., `streamlit` not found)**  
  → Ensure you're using the correct Python environment (`venv`) and `pip install -r requirements.txt` completed successfully.

---

## Project Structure
src/
├── app.py # Main Streamlit UI
├── agents/
│ └── loop_agent.py # Core Reasoning Agent
├── services/
│ ├── embedding.py # GeminiEmbeddings wrapper
│ ├── vectore_store.py # FAISS / Qdrant retrieval
├── tools/
│ └── doc_search.py, etc. # External tools
├── utils/
│ └── langfuse_wrapper.py # Optional Langfuse tracing


---

## References

- [Google Generative AI SDK (Python)](https://pypi.org/project/google-generativeai/)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai)
- [Agent Development Kit (ADK)](https://ai.google.dev/docs/agents/overview)







