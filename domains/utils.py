from domains.settings import config_settings
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import AzureChatOpenAI
from typing import List, Union, Any
import time
from typing import Callable
import functools
import asyncio
from loguru import logger

from langchain_groq import ChatGroq

def calculate_and_log_time(func: Callable) -> Callable:
    """
    Decorator to calculate and log the execution time of both sync and async functions.

    Args:
        func: The function to be wrapped

    Returns:
        Wrapped function with execution time logging
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            logger.debug(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            logger.debug(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def get_chat_model(model_key: str = "CHAT_MODEL_NAME", temperature: float = 0.0) -> Union[ChatOpenAI, AzureChatOpenAI, Any]:
    """
    Function to get the chat model based on the provided key.
    """
    if config_settings.LLM_SERVICE_TYPE == "openai":
        return ChatOpenAI(
            model=config_settings.LLMS.get(
                model_key, ""
            ),
            temperature=temperature,
            streaming=True,
        )

    elif config_settings.LLM_SERVICE_TYPE == "azure_openai":
        return AzureChatOpenAI(
            azure_endpoint=config_settings.AZURE_OPENAI_SETTINGS[model_key]["ENDPOINT"],
            azure_deployment=config_settings.AZURE_OPENAI_SETTINGS[model_key][
                "DEPLOYMENT"
            ],
            api_key=config_settings.AZURE_OPENAI_SETTINGS[model_key]["API_KEY"],
            api_version=config_settings.AZURE_OPENAI_SETTINGS[model_key]["API_VERSION"],
            model=config_settings.LLMS.get(model_key, ""),
            temperature=temperature,
        )

    elif config_settings.LLM_SERVICE_TYPE == "groq":
        return ChatGroq(
            model="llama-3.2-11b-vision-preview",
            temperature=temperature,
            streaming=True,
        )


if __name__ == "__main__":
    print(get_chat_model().invoke("Hi"))

