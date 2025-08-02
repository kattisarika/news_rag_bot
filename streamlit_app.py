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
    articles = get_news_articles(source="ESPN")

# Display articles
for i, article in enumerate(articles[:5]):
    st.markdown(f"**{i+1}.** {article}")

def load_news():
    with open("news_data.txt", "r") as f:
        news = f.read().split("\n\n")
    return news[:10]  # top 10 stories

# Load news
st.title("🗞️ News Q&A Bot")
st.subheader("Latest Headlines:")
for item in load_news():
    st.markdown(f"👉 {item}")

# User Q&A section
st.markdown("---")
st.subheader("Ask a question about the news:")
question = st.text_input("Enter your question")

if question:
    # Run your existing QA chain (import it from app.py)
    from app import qa_chain
    response = qa_chain.run(question)
    st.markdown("### 🤖 Answer:")
    st.write(response)
