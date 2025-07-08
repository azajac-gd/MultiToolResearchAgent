import logging
import streamlit as st
from agent import root_agent 
from vertexai.preview.reasoning_engines import AdkApp
from critique import run_critique

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def agent_loop(user_query: str, max_iterations: int = 3) -> str:
    current_query = user_query
    history = []

    for i in range(max_iterations):
        result = ""
        for event in app.stream_query(user_id="id", message=current_query):
            try:
                result = event["content"]["parts"][0]["text"]
            except:
                result = "No response from agent."

        history.append((current_query, result))

        critique = run_critique(current_query, result)
        logging.info(f"Critique for query '{current_query}': {critique}")
        if critique.get("stop", True):
            return result

        follow_ups = critique.get("follow_up_questions", [])
        if not follow_ups:
            return result

        current_query = current_query + " " + " ".join(follow_ups)

    return result

app = AdkApp(agent=root_agent)

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Type your research question here..."):
    with st.spinner("Thinking..."):
        final_reply = agent_loop(prompt)
        st.session_state.history.append((prompt, final_reply))

for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)