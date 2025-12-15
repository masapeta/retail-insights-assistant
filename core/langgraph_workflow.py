from langgraph.graph import StateGraph, END
from core.state_schema import State

from agents.language_to_query_agent import language_to_query_agent
from agents.validation_agent import validation_agent
from agents.data_extraction_agent import data_extraction_agent
from agents.rag_retrieval_agent import rag_retrieval_agent
from agents.insight_generation_agent import insight_generation_agent


# -------------------------------------------------------------
# Build LangGraph pipeline for hybrid multi-agent workflow
# -------------------------------------------------------------
graph = StateGraph(State)

graph.add_node("parse", language_to_query_agent)
graph.add_node("validate", validation_agent)
graph.add_node("extract", data_extraction_agent)
graph.add_node("rag", rag_retrieval_agent)
graph.add_node("insight", insight_generation_agent)

graph.set_entry_point("parse")
graph.add_edge("parse", "validate")
graph.add_edge("validate", "extract")
graph.add_edge("extract", "rag")
graph.add_edge("rag", "insight")
graph.add_edge("insight", END)

workflow = graph.compile()

def run_assistant(state: dict):
    return workflow.invoke(state)
