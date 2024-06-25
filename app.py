import dropbox
import streamlit as st
import poppler
import os
import time
from pdf2image import convert_from_path
import pytesseract
from embedchain import App

with st.sidebar:
    st.title("HIT AI")
    st.caption("🚀 Powered by Afrinity Technologies!")
    huggingface_access_token = st.text_input("Hugging face Token", key="chatbot_api_key", type="password")
    dropbox_access_token = st.text_input("Dropbox Access Token", key="dropbox_api_key", type="password")

    if st.button("➕Start New Chat"):
      st.session_state.messages = [
          {
              "role": "assistant",
              "content": "Hi! I'm HIT AI Assistant. Ask me anything :)"
          }
      ]
      st.experimental_rerun()
    if st.button("Reload Knowledge Base"):
        import dropbox
        import os
        from pdf2image import convert_from_path
        import pytesseract
        import sentence_transformers
        import poppler
        from embedchain import App

        # Replace this with your HF token
        os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.session_state.chatbot_api_key
        os.environ[
            "DROPBOX_ACCESS_TOKEN"] = st.session_state.dropbox_api_key
        config = {
            'llm': {
                'provider': 'huggingface',
                'config': {
                    'model': 'mistralai/Mistral-7B-Instruct-v0.2',
                    'top_p': 0.5
                }
            },
            'embedder': {
                'provider': 'huggingface',
                'config': {
                    'model': 'sentence-transformers/all-mpnet-base-v2'
                }
            }
        }
        app = App.from_config(config=config)
        # Dropbox API access token
        if __name__ == '__main__':
            ACCESS_TOKEN = st.session_state.dropbox_api_key

            # Create a Dropbox client
            dbx = dropbox.Dropbox(ACCESS_TOKEN)

            # Dropbox folder path
            dropbox_folder_path = '/test2'

            # Local folder to save downloaded PDFs
            local_folder_path = './downloaded_pdfs'
            os.makedirs(local_folder_path, exist_ok=True)


            # List and download PDFs

            # section2
            def list_and_download_pdfs(dbx, folder_path):
                pdf_files = []
                result = dbx.files_list_folder(folder_path)
                while result.entries:
                    for entry in result.entries:
                        if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):

                            local_file_path = os.path.join(local_folder_path, entry.name)
                            if not os.path.exists(local_file_path):
                                pdf_files.append(entry.name)
                            with open(local_file_path, "wb") as f:
                                metadata, res = dbx.files_download(entry.path_lower)
                                f.write(res.content)
                    if result.has_more:
                        result = dbx.files_list_folder_continue(result.cursor)
                    else:
                        break
                return pdf_files


            pdf_files = list_and_download_pdfs(dbx, dropbox_folder_path)
            print(f"Downloaded PDFs: {pdf_files}")


            # Convert PDFs to text using OCR
            def pdf_to_text(pdf_path):
                pages = convert_from_path(pdf_path, 300)
                texts = [pytesseract.image_to_string(page) for page in pages]
                return "\n".join(texts)


            pdf_texts = []
            for pdf_file in pdf_files:
                local_pdf_path = os.path.join(local_folder_path, pdf_file)
                text = pdf_to_text(local_pdf_path)
                print("Added")
                pdf_texts.append((pdf_file, text))

            # section 3
            app = App.from_config(config=config)
            # Add extracted texts to EmbedChain
            for pdf_file, text in pdf_texts:
                print("something is being added \n")
                app.add(text, data_type='text')

            app.add("/gen2", data_type="dropbox")
            # Query the embedded texts


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
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.session_state.chatbot_api_key
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
