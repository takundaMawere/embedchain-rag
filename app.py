import dropbox 
from rag import app
import streamlit as st
import poppler
import os
import time
from pdf2image import convert_from_path
import pytesseract


with st.sidebar:
    st.title("HIT AI")
    st.caption("🚀 Powered by Afrinity Technologies!")
    if st.button("➕Start New Chat"):
      st.session_state.messages = [
          {
              "role": "assistant",
              "content": "Hi! I'm HIT AI Assistant. Ask me anything :)"
          }
      ]
      st.experimental_rerun()
    
        
def extract_answer(response):
    # Split the response by lines
    lines = response.split('\n')

    # Find the line that starts with "Answer:" to get the answer section
    answer_index = next(i for i, line in enumerate(lines) if line.startswith("Answer:"))

    # Return the part of the response starting from the answer index + 1 (to skip "Answer:")
    answer = '\n'.join(lines[answer_index + 1:])

    return answer.strip()

def response_generator(resp):
    for word in resp.split():
        yield word + " "
        time.sleep(0.05)
# # Sample usage
# response = app.query("Where is Chapati located")
# answer = extract_answer(response)
# print(answer)

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
    # if not st.session_state.chatbot_api_key:
    #     st.error("Please enter your Hugging Face Access Token")
    #     st.stop()

    # os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.session_state.chatbot_api_key
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"
    # app = App.from_config(config=config)

    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            app.add(prompt)
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

        for response in extract_answer(app.query(prompt)):
            msg_placeholder.empty()
            full_response += response

        st.write_stream(response_generator(full_response))
        # msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# query = "can you give me a sample question for database systems"
# response = app.query(query)
# print(extract_answer(response))