import base64
import asyncio
import pprint
from typing import Union, Any, Optional
from domains.utils import get_chat_model
from langchain_core.messages import HumanMessage
from functools import lru_cache
from langchain.tools import Tool
from domains.workflows.handler import retry_with_backoff
from domains.workflows.prompts import IMAGE_SUMMARY_GENERATION_PROMPT
from domains.workflows.prompts import initialize_image_classification_prompt
from domains.injestion.doc_loader import process_image
from langchain_core.output_parsers import JsonOutputParser
from domains.utils import calculate_and_log_time
from loguru import logger


class ImageProcessingError(Exception):
    """Custom exception for image processing errors"""
    pass


class ModelProcessingError(Exception):
    """Custom exception for model processing errors"""
    pass


@lru_cache(maxsize=128)
def get_cached_model(model_name: str, temperature: float) -> Any:
    """Caches and returns the chat model instance"""
    return get_chat_model(model_name, temperature)


@calculate_and_log_time
async def load_image(image_file_path: str, process_type: str, image_type: Optional[str] = None) -> dict[str, Any]:
    """Loads and processes an image file.

    Args:
        image_file_path: Path to the image file
        process_type: Type of processing to apply
        image_type: Optional image format type

    Returns:
        Dictionary containing processed image data

    Raises:
        ImageProcessingError: If image loading or processing fails
    """
    try:
        return await process_image(image_file_path, process_type, image_type)
    except Exception as e:
        raise ImageProcessingError(f"Failed to load image: {str(e)}") from e


class InvalidInputError(Exception):
    """Custom exception for invalid input validation"""
    pass


@retry_with_backoff(max_retries=3, initial_delay=2, backoff_factor=2, max_delay=10)
@calculate_and_log_time
async def summarize_image_content(image_contents: Union[str, dict[str, Any]]) -> str:
    """Generates a summary of image content using a language model.

    Args:
        image_contents: Image content as URL string or dict with URL

    Returns:
        String containing image summary

    Raises:
        ModelProcessingError: If summarization fails
    """
    try:
        chat_model = get_cached_model("CHAT_MODEL_NAME", 0.0)

        if not chat_model:
            raise ModelProcessingError("Failed to initialize chat model")

        image_url = image_contents if isinstance(image_contents, str) else image_contents.get("url")
        if not image_url:
            raise InvalidInputError("Invalid image URL format")

        summary_response = await chat_model.ainvoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": IMAGE_SUMMARY_GENERATION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                    ]
                )
            ],
        )
        return summary_response.content

    except Exception as e:
        raise ModelProcessingError(f"Failed to summarize image: {str(e)}") from e



@calculate_and_log_time
async def classify_image_content(image_summary: Union[str, dict[str, Any]]) -> dict[str, Any]:
    """Classifies image content based on its summary using a language model.

    Args:
        image_summary: Text summary or dict containing image information

    Returns:
        Dictionary containing classification results

    Raises:
        ModelProcessingError: If classification fails
    """
    try:
        logger.debug(f"Classifying image content: {image_summary}")

        llm = get_cached_model("CHAT_MODEL_NAME", 0.0)
        if not llm:
            raise ModelProcessingError("Failed to initialize language model")

        chain = initialize_image_classification_prompt() | llm | JsonOutputParser()
        classified_response = await chain.ainvoke({"image_summary": image_summary})

        if classified_response:
            classified_response['image_summary'] = image_summary

        return classified_response

    except Exception as e:
        raise ModelProcessingError(f"Failed to classify image: {str(e)}") from e


if __name__ == "__main__":
    async def main():
        try:
            image_file_path = "/Users/mohitverma/Downloads/2024-08-16T192529Z_1430337378_RC23H9ADLF7Q_RTRMADP_3_UKRAINE-CRISIS-RUSSIA-BORDER-1400x984.jpg"
            res = await load_image(image_file_path, "base64", 'jpg')
            summary = await summarize_image_content(res.get("image_url"))
            classification = await classify_image_content(summary)
            pprint.pprint(classification)
        except (ImageProcessingError, ModelProcessingError) as e:
            logger.error(f"Processing failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

    asyncio.run(main())