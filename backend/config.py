from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
from pathlib import Path

# .env ka exact path
ENV_PATH = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        extra="ignore"
    )
    
    truefoundry_api_key: str
    truefoundry_base_url: str = "https://llm-gateway.truefoundry.com/api/inference/openai"
    llm_model: str = "internal-bedrock/sonnet-46"
    chroma_persist_dir: str = "./chroma_db"
    langchain_api_key: Optional[str] = None

settings = Settings()