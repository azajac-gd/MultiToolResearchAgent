import streamlit as st
import logging
from vertexai.preview.reasoning_engines import AdkApp
from loop_agent import research_agent

#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = AdkApp(agent=research_agent)

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")
extended_mode = st.toggle("Extended Mode", value=False)

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Enter your research question..."):
    with st.spinner("Thinking..."):
        response = ""
        i = 0
        for event in app.stream_query(
            user_id="user-123",
            message=prompt,
            #inputs={"extended_mode": extended_mode}

        ):  
            print(i)
            response = event.get("content", {}).get("parts", [{}])[0].get("text", "")
            print(response)
            #logging.info(f"Response part: {response}")
            if i == 4:
                #logging.info(f"Final response: {response}")
                print(response)
                st.session_state.history.append((prompt, response))
            i += 1


for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg, unsafe_allow_html=True)

if extended_mode and st.session_state.history:
    if st.button("Save Last Answer as File"):
        last_question, last_answer = st.session_state.history[-1]
        filename = f"research_response.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Q: {last_question}\n\nA: {last_answer}")
        st.success(f"Saved to {filename}")
