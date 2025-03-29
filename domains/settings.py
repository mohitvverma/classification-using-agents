from pydantic_settings import BaseSettings
from typing import ClassVar
import os


class Settings(BaseSettings):
    # openai
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_CHAT_BASE_URL: str = os.environ.get(
        "OPENAI_CHAT_BASE_URL", "https://api.openai.com/v1/chat/completions"
    )
    THREASHOLD_MESSAGE_TO_SUMMARIZE: int = int(
        os.environ.get("THREASHOLD_MESSAGE_TO_SUMMARIZE", 10)
    )
    OPENAI_EMBEDDING_MODEL_NAME: str = os.environ.get(
        "OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-3-small"
    )

    # LLM Service
    LLM_SERVICE_TYPE: str = os.environ.get("LLM_SERVICE", "openai")

    # Modular Model Names
    LLMS: ClassVar[dict] = {
        "CHAT_MODEL_NAME": os.environ.get("OPENAI_CHAT_MODEL_NAME", "gpt-4o"),
        "SUMMARIZE_LLM_MODEL": os.environ.get("SUMMARIZE_LLM_MODEL", "gpt-4o"),
        "EMBEDDING_MODEL_NAME": os.environ.get(
            "EMBEDDING_MODEL_NAME", "text-embedding-3-small"
        ),
        "CLASSIFICATION_MODEL_NAME": os.environ.get("CLASSIFICATION_MODEL", "gpt-4o"),
        "OPTIMIZED_QUESTION_MODEL": os.environ.get("OPTIMIZED_QUESTION_MODEL", "gpt-4o"),
        "CHAT_STREAMING_MODEL_NAME": os.environ.get("CHAT_STREAMING_MODEL_NAME", "gpt-4o"),
    }

    AZURE_OPENAI_SETTINGS: ClassVar[dict] = {
        "LLM_MODEL_NAME": {
            "ENDPOINT": os.environ.get("AZURE_ENDPOINT_LLM_MODEL_NAME", ""),
            "API_KEY": os.environ.get("AZURE_API_KEY_LLM_MODEL_NAME", ""),
            "DEPLOYMENT": os.environ.get("AZURE_DEPLOYMENT_LLM_MODEL_NAME", ""),
            "API_VERSION": os.environ.get("AZURE_API_VERSION_LLM_MODEL_NAME", ""),
            "OPTIMIZED_QUESTION_MODEL": os.environ.get("OPTIMIZED_QUESTION_MODEL", "gpt-4o-mini"),
        },
        "CHAT_MODEL_NAME": {
            "ENDPOINT": os.environ.get("CHAT_MODEL_NAME", ""),
            "API_KEY": os.environ.get("CHAT_MODEL_NAME", ""),
            "DEPLOYMENT": os.environ.get("CHAT_MODEL_NAME", ""),
            "API_VERSION": os.environ.get("CHAT_MODEL_NAME", ""),
        },
        "CHAT_STREAMING_MODEL_NAME": {
            "ENDPOINT": os.environ.get("CHAT_STREAMING_MODEL_NAME", ""),
            "API_KEY": os.environ.get("CHAT_STREAMING_MODEL_NAME", ""),
            "DEPLOYMENT": os.environ.get("CHAT_STREAMING_MODEL_NAME", ""),
            "API_VERSION": os.environ.get("CHAT_STREAMING_MODEL_NAME", ""),
        }
    }

    GOOGLE_GEMINI_SETTINGS: ClassVar[dict] = {
        "CHAT_MODEL_NAME": os.environ.get("OPENAI_CHAT_MODEL_NAME", "gpt-4o"),
        "SUMMARIZE_LLM_MODEL": os.environ.get("SUMMARIZE_LLM_MODEL", "gpt-4o"),
        "EMBEDDING_MODEL_NAME": os.environ.get(
            "OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-3-small"
        ),
        "CLASSIFICATION_MODEL": os.environ.get("CLASSIFICATION_MODEL", "gpt-4o"),
        "OPTIMIZED_QUESTION_MODEL": os.environ.get("OPTIMIZED_QUESTION_MODEL", "gpt-4o"),
        "CHAT_STREAMING_MODEL_NAME": os.environ.get("OPENAI_CHAT_STREAMING_MODEL", "gpt-4o"),
    }


config_settings = Settings()
