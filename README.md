# Multi-Tool Research Agent 

A conversational research assistant powered by Google Vertex AI's Reasoning Engine (`AdkApp`) and Streamlit UI.  
Supports extended mode for saving long-form synthesized reports.  
Runs locally.

---

## Features

- Powered by Google Vertex AI (ADK Reasoning Engine)
- Streamlit-based chat interface
- Extended mode for long-form reports (toggle)
- Dockerized with GCP authentication via ADC
- Automatically stores chat history in session state

---

## Requirements

- Python 3.10+
- Google Cloud project with Vertex AI enabled
- `gcloud` CLI with authenticated credentials
- (Optional) Docker installed for containerized deployment

---

## Installation (Local)

1. Clone the repository

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Authenticate with Google Cloud:

    ```bash
    gcloud auth application-default login
    ```

5. Run the app:

    ```bash
    streamlit src/run app.py
    ```

