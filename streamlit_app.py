import streamlit as st
from app import qa_chain
st.title("NEWS RAG BOT")


def load_news():
    with open("news_data.txt", "r") as f:
        news = f.read().split("\n\n")
    return news[:10]  # top 10 stories

# Load news
st.title("🗞️ TOI News Q&A Bot")
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
