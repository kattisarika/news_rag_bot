import streamlit as st
from app import qa_chain
from app import get_news_articles

st.title("Process Automation")
st.text("INTEGRATING USER STORIES TO CURSOR OR LOVABLE =====>  GENERATING CODE THROUGH THESE PLATFORMS ===========> DEPLOYING THE APP ON AWS OR HEROKU ")
st.text("INTEGRATING JIRA BUG FILING TO CURSOR OR LOVABLE =====>  GENERATING CODE THROUGH THESE PLATFORMS ===========> DEPLOYING THE APP ON AWS OR HEROKU ")


st.title("NEWS PORTAL")


option_map = {
    "Times of India": "TOI",
    "NY Times": "NY TIMES",
    "BBC": "BBC",
    "Weather": "WEATHER",
    "Countries (GraphQL)": "GRAPHQL"  
}

news_source_label = st.radio("Choose your news source:", list(option_map.keys()))
source_key = option_map[news_source_label]

articles = get_news_articles(source=source_key)

if articles:
    for i, article in enumerate(articles[:10]):
        st.markdown(f"**{i+1}.** {article}", unsafe_allow_html=True)
else:
    st.write("No articles found for the selected source.")


