import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Agent Flow"
    DEBUG: bool = True
    
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "mysql")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USERNAME", "agent_flow")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "secret")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "agent_flow")
    
    @property
    def DATABASE_URI(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    # Temporal
    TEMPORAL_HOST: str = os.getenv("TEMPORAL_HOST", "temporal:7233")
    TEMPORAL_NAMESPACE: str = os.getenv("TEMPORAL_NAMESPACE", "default")
    TEMPORAL_TASK_QUEUE: str = os.getenv("TEMPORAL_TASK_QUEUE", "agent-flow-tasks")

    # AI (LiteLLM)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
