import streamlit as st
from embedchain.store.assistants import AIAssistant
from rag import assistant
import os
import uuid
import chromadb
from chromadb.config import Settings
client = chromadb.Client(Settings(anonymized_telemetry=False))
os.environ["GOOGLE_API_KEY"] = "AIzaSyAYlgd7yepzspC78xfMWm0fBHUT3j6ZPuE"

st.title("Alex")
st.caption("🚀 Powered by afrAInity Technologies!")

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
