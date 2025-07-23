
import streamlit as st
import logging
from agents.my_agent import get_research_agent_langgraph

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")

extended_mode = st.toggle("Extended Mode", value=False)

agent_app = get_research_agent_langgraph(extended_mode=extended_mode)

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Enter your research question..."):
    with st.spinner("Thinking..."):
        initial_state = {
            "question": prompt,
            "tool_results": [],
            "retry_count": 0,
        }

        final_state = agent_app.invoke(initial_state)
        response = final_state.get("synthesis", "No response generated.")

        st.session_state.history.append((prompt, response))

for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg, unsafe_allow_html=True)
