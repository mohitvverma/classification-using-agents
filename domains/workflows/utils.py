from langchain_core.messages import HumanMessage


def summary_generation_prompt(
        image_url,
        template
):
    return [
        HumanMessage(
            content=[
                {"type": "text", "text": template},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                },
            ]
        )
    ]


class ImageProcessingError(Exception):
    """Custom exception for image processing errors"""
    pass


class ModelProcessingError(Exception):
    """Custom exception for model processing errors"""
    pass

class InvalidInputError(Exception):
    """Custom exception for invalid input validation"""
    pass
