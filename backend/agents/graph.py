from typing import TypedDict, Optional, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    report_text: str
    report_id: str
    patient_profile: dict
    language: str
    retrieved_chunks: list[str]
    analysis_result: Optional[str]
    diet_result: Optional[str]
    comparison_result: Optional[str]
    final_response: Optional[str]
    sources: list[str]
    errors: list[str]

graph = StateGraph(AgentState)

from backend.agents.analyzer_agent import analyzer_node
from backend.agents.diet_agent import diet_node
from backend.agents.comparator_agent import comparator_node

def synthesizer_node(state: AgentState) -> AgentState:
    state['final_response'] = f"Analysis: {state['analysis_result']}\nDiet: {state['diet_result']}\nComparison: {state['comparison_result']}"
    return state

graph.add_node("analyzer", analyzer_node)
graph.add_node("diet", diet_node)
graph.add_node("comparator", comparator_node)
graph.add_node("synthesizer", synthesizer_node)

graph.add_edge(START, "analyzer")
graph.add_edge("analyzer", "diet")
graph.add_edge("diet", "comparator")
graph.add_edge("comparator", "synthesizer")
graph.add_edge("synthesizer", END)

compiled_graph = graph.compile()