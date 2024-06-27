import streamlit as st
import os
# from rag import assistant
from embedchain.store.assistants import AIAssistant
os.environ["GOOGLE_API_KEY"] = "AIzaSyDRiI5PgPjGCoWOjOZxSf0a5P_6lirLPQc"
assistant = AIAssistant(assistant_id="aa9af753-e2ac-403d-b0e3-121491f0eeaa")
def extract_answer(response):
    # Split the response by lines
    lines = response.split('\n')

    # Find the line that starts with "Answer:" to get the answer section
    answer_index = next(i for i, line in enumerate(lines) if line.startswith("Answer:"))

    # Return the part of the response starting from the answer index + 1 (to skip "Answer:")
    answer = '\n'.join(lines[answer_index + 1:])

    return answer.strip()


st.title("HIT AI")
st.caption("🚀 Powered by Afrinity Technologies!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
        Hi! I'm HIT AI Assistant. Ask me anything :)
        """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    msg_placeholder = st.empty()
    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            assistant.add(prompt)
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        for response in assistant.chat(prompt):
            msg_placeholder.empty()
            full_response += response

        st.write(full_response)
        # msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

