import streamlit as st
from agent import root_agent 
from vertexai.preview.reasoning_engines import AdkApp


app = AdkApp(agent=root_agent)



st.set_page_config(page_title="Research Agent", layout="centered")

st.markdown(
    """
    <style>
        .stChatMessage { margin-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Research Agent")

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Type your research question here..."):
    with st.spinner("Thinking..."):
        reply = None

        for event in app.stream_query(user_id="5", message=prompt):
            if hasattr(event, "is_final_response") and event.is_final_response():
                content = event.content
                if content and content.parts:
                    part = content.parts[0]
                    reply = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)

        reply = reply or "No response from agent."
    st.session_state.history.append((prompt, reply))

for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
