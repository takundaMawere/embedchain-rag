import os
from embedchain import App
from embedchain.store.assistants import AIAssistant
from bs4 import BeautifulSoup

os.environ["GOOGLE_API_KEY"] = "AIzaSyDRiI5PgPjGCoWOjOZxSf0a5P_6lirLPQc"
assistant = AIAssistant(
    name="HIT AI Assistant",
    instructions="Your name is HIT AI Assistant. Write about the Harare Institute of Technology (HIT) only. Avoid mentioning any other universities or institutes. Ask me anything related to HIT.",
    yaml_path="config.yaml",
    data_sources = [{"source": "./Knowledge", "data_type": "directory"},{"source": "https://www.hit.ac.zw/post-sitemap.xml", "data_type": "sitemap"},{"source": "https://www.hit.ac.zw/page-sitemap.xml", "data_type": "sitemap"}])
# os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"
#
# config = {
#     'llm': {
#         'provider': 'huggingface',
#         'config': {
#             'model': 'mistralai/Mistral-7B-Instruct-v0.2',
#             'top_p': 0.5
#         }
#     },
#     'embedder': {
#         'provider': 'huggingface',
#         'config': {
#             'model': 'sentence-transformers/all-mpnet-base-v2'
#         }
#     }
# }

# app = App.from_config(config_path="config.yaml")
# # app = App.from_config(config=config)
# if __name__ == '__main__':
#     app.add("./Knowledge", data_type="directory")