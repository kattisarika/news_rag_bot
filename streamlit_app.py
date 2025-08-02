import streamlit as st
from app import qa_chain
from app import get_news_articles
st.title("NEWS RAG BOT")

# Add a radio button for source selection
news_source = st.radio("Choose your news source:", ("Times of India", "BBC","ESPN"))

# Get news based on source
if news_source == "Times of India":
    articles = get_news_articles(source="TOI")
elif news_source == "BBC":
    articles = get_news_articles(source="BBC")
else:
    articles = get_news_articles(source="espn")

# Display articles
for i, article in enumerate(articles[:10]):
    st.markdown(f"**{i+1}.** {article}")


