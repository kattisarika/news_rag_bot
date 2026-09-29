from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app import (
    fetch_from_toi,
    fetch_from_bbc,
    fetch_from_nytimes,
    fetch_sample_weather,
    fetch_from_graphql
)


class AgentState(TypedDict):
    query: str
    route: str
    result: list
    error: str
    retry_count: int
