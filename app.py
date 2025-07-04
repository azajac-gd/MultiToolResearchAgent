import streamlit as st
from agent import root_agent 
from vertexai.preview.reasoning_engines import AdkApp


app = AdkApp(agent=root_agent)

#session_service = VertexAiSessionService(os.getenv("PROJECT_ID"), os.getenv("LOCATION"))


st.set_page_config(page_title="Research Agent", layout="centered")

st.title("Research Agent")

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Type your research question here..."):
    with st.spinner("Thinking..."):
        reply = None

        for event in app.stream_query(user_id="id", message=prompt):
            print(event)
            try:
                text = event["content"]["parts"][0]["text"]
                reply = text
            except:
                reply = "No response from agent."

    st.session_state.history.append((prompt, reply))

for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
