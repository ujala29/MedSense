from backend.config import settings
from openai import AsyncOpenAI
from backend.vectorstore.retriever import retrieve_context
from backend.agents.graph import AgentState

llm_client = AsyncOpenAI(
    api_key=settings.truefoundry_api_key,
    base_url=settings.truefoundry_base_url,
)

async def analyzer_node(state: AgentState) -> AgentState:
    query = state['report_text'][:200]
    retrieved = retrieve_context(query, state['report_id'])
    state['retrieved_chunks'] = retrieved
    prompt = f"""
    Analyze the medical report. List all lab values, flag abnormalities with [ABNORMAL], cite sources.
    Language: {state['language']}
    Report text: {state['report_text']}
    Retrieved chunks: {' '.join(retrieved)}
    """
    response = await llm_client.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )
    state['analysis_result'] = response.choices[0].message.content
    state['sources'] = retrieved
    return state