import streamlit as st

from agent import news_agent


# =========================================================
# PAGE
# =========================================================

st.title("Agentic News Assistant")

st.write(
    "Ask me about BBC, Times of India, "
    "New York Times, weather, or countries."
)


# =========================================================
# USER QUESTION
# =========================================================

query = st.text_input(
    "What would you like to know?"
)


# =========================================================
# ASK AGENT
# =========================================================

if st.button("Ask Agent"):

    if query:

        initial_state = {

            "query": query,

            "route": "",

            "result": [],

            "error": "",

            "retry_count": 0
        }


        # Execute LangGraph

        response = news_agent.invoke(
            initial_state
        )


        # Show selected route

        st.write(
            f"**Agent selected:** "
            f"{response['route']}"
        )


        # Display results

        results = response.get(
            "result",
            []
        )


        if results:

            for item in results:

                st.markdown(item)

        else:

            st.warning(
                "No results returned."
            )

    else:

        st.warning(
            "Please enter a question."
        )
