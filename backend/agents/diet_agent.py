from backend.config import settings
from openai import AsyncOpenAI
from backend.agents.graph import AgentState

llm_client = AsyncOpenAI(
    api_key=settings.truefoundry_api_key,
    base_url=settings.truefoundry_base_url,
)

async def diet_node(state: AgentState) -> AgentState:
    prompt = f"""
    Generate 7-day diet plan based on analysis: {state['analysis_result']}
    Patient profile: {state['patient_profile']}
    Language: {state['language']}
    """
    response = await llm_client.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )
    state['diet_result'] = response.choices[0].message.content
    return state