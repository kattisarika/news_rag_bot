import os
import requests
import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from chromadb.config import Settings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import streamlit as st
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
print("Loaded OpenAI key:", bool(openai_api_key))  # TEMP: for debugging

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

def get_news_articles(source="TOI"):
    if source == "TOI":
        return fetch_from_toi()
    elif source == "BBC":
        return fetch_from_bbc()
    elif source == "NY TIMES":
        return fetch_from_nytimes()    
    else:
        return []





def fetch_from_toi():
    import requests
    from bs4 import BeautifulSoup

    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll("item")
    return [item.title.text + ". " + item.description.text for item in items]

   
def fetch_from_bbc():
    import requests
    from bs4 import BeautifulSoup

    url = "http://feeds.bbci.co.uk/news/rss.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll("item")
    return [item.title.text + ". " + item.description.text for item in items]

def fetch_from_nytimes():
    import requests
    from bs4 import BeautifulSoup

    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll("item")
    return [item.title.text + ". " + item.description.text for item in items]

# Scrape and process
news_text = scrape_news()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_text(news_text)


# After loading your texts:
embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_texts(texts, embedding=embeddings)


# Define LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Expose QA chain for external use
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever()
)

if __name__ == "__main__":
    print("Scraped news and created vector store.")
    print("You can now run queries via the Streamlit app.")

