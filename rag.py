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