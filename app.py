import os
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from chromadb.config import Settings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
print("Loaded OpenAI key:", bool(openai_api_key))  # TEMP: for debugging

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

def scrape_news():
    url = "https://timesofindia.indiatimes.com"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all("a", href=True)
    news = []
    for a in articles:
        text = a.get_text(strip=True)
        href = a['href']
        if text and '/articleshow/' in href:
            full_link = url + href if not href.startswith("http") else href
            news.append(f"{text} ({full_link})")
        if len(news) >= 10:
            break
    return "\n".join(news)

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

