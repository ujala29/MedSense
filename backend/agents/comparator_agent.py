from backend.config import settings
from openai import AsyncOpenAI
from backend.vectorstore.retriever import retrieve_historical
from backend.agents.graph import AgentState

llm_client = AsyncOpenAI(
    api_key=settings.truefoundry_api_key,
    base_url=settings.truefoundry_base_url,
)

async def comparator_node(state: AgentState) -> AgentState:
    patient_id = state['patient_profile'].get('patient_id')
    historical = retrieve_historical(patient_id)
    if not historical:
        state['comparison_result'] = "No previous reports found for comparison."
    else:
        prompt = f"""
        Compare current report with historical: {' '.join(historical)}
        Current: {state['report_text']}
        Language: {state['language']}
        """
        response = await llm_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
        )
        state['comparison_result'] = response.choices[0].message.content
    return state