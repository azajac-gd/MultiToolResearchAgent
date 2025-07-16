import streamlit as st
import logging
from vertexai.preview.reasoning_engines import AdkApp
from agents.loop_agent import get_research_agent

logging.getLogger("opentelemetry").setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")
extended_mode = st.toggle("Extended Mode", value=False)

research_agent = get_research_agent(extended_mode=extended_mode)
app = AdkApp(agent=research_agent)


if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Enter your research question..."):
    with st.spinner("Thinking..."):
        response = ""
        response_from_synthesizer = None

        for event in app.stream_query(
            user_id="user-123",
            message=prompt,
        ):  
            content = event.get("content", {})
            step_name = event.get("author", "")
            #print(f"Processing step: {step_name}")
            text = content.get("parts", [{}])[0].get("text", "")
            #print(f"Step content: {text}")

            if step_name == "Synthesizer" and text:
                response_from_synthesizer = text

        if response_from_synthesizer:
            st.session_state.history.append((prompt, response_from_synthesizer))
        else:
            st.session_state.history.append((prompt, "No response generated."))


for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg, unsafe_allow_html=True)

# if extended_mode and st.session_state.history:
#     if st.button("Save to file"):
#         last_question, last_answer = st.session_state.history[-1]
#         filename = f"research_response.txt"
#         with open(filename, "w", encoding="utf-8") as f:
#             f.write(f"Q: {last_question}\n\nA: {last_answer}")
#         st.success(f"Saved to {filename}")
