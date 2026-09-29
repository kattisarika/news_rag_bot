from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app import (
    fetch_from_toi,
    fetch_from_bbc,
    fetch_from_nytimes,
    fetch_sample_weather,
    fetch_from_graphql
)


# =========================================================
# STEP 1: DEFINE AGENT STATE
# =========================================================

class AgentState(TypedDict):

    query: str
    route: str
    result: list
    error: str
    retry_count: int


# =========================================================
# STEP 2: ROUTER NODE
# =========================================================

def router_node(state: AgentState):

    query = state["query"].lower()

    if "weather" in query:

        route = "WEATHER"

    elif (
        "country" in query
        or "capital" in query
    ):

        route = "GRAPHQL"

    elif "bbc" in query:

        route = "BBC"

    elif (
        "new york times" in query
        or "nyt" in query
    ):

        route = "NY TIMES"

    elif (
        "times of india" in query
        or "india news" in query
        or "toi" in query
    ):

        route = "TOI"

    else:

        # Default route
        route = "BBC"

    return {
        "route": route
    }


# =========================================================
# STEP 3: TOOL NODES
# =========================================================

def bbc_node(state: AgentState):

    result = fetch_from_bbc()

    return {
        "result": result
    }


def toi_node(state: AgentState):

    result = fetch_from_toi()

    return {
        "result": result
    }


def nyt_node(state: AgentState):

    result = fetch_from_nytimes()

    return {
        "result": result
    }


def weather_node(state: AgentState):

    result = fetch_sample_weather()

    return {
        "result": result
    }


def country_node(state: AgentState):

    result = fetch_from_graphql()

    return {
        "result": result
    }


# =========================================================
# STEP 4: CONDITIONAL ROUTING
# =========================================================

def choose_route(state: AgentState):

    return state["route"]


# =========================================================
# STEP 5: BUILD LANGGRAPH
# =========================================================

builder = StateGraph(AgentState)


# Add nodes

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "BBC",
    bbc_node
)

builder.add_node(
    "TOI",
    toi_node
)

builder.add_node(
    "NY TIMES",
    nyt_node
)

builder.add_node(
    "WEATHER",
    weather_node
)

builder.add_node(
    "GRAPHQL",
    country_node
)


# =========================================================
# START -> ROUTER
# =========================================================

builder.add_edge(
    START,
    "router"
)


# =========================================================
# ROUTER -> CORRECT TOOL
# =========================================================

builder.add_conditional_edges(
    "router",

    choose_route,

    {
        "BBC": "BBC",
        "TOI": "TOI",
        "NY TIMES": "NY TIMES",
        "WEATHER": "WEATHER",
        "GRAPHQL": "GRAPHQL"
    }
)


# =========================================================
# TOOL -> END
# =========================================================

builder.add_edge(
    "BBC",
    END
)

builder.add_edge(
    "TOI",
    END
)

builder.add_edge(
    "NY TIMES",
    END
)

builder.add_edge(
    "WEATHER",
    END
)

builder.add_edge(
    "GRAPHQL",
    END
)


# =========================================================
# COMPILE GRAPH
# =========================================================

news_agent = builder.compile()
