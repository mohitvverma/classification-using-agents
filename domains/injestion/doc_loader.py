# import base64
# import re
# from pathlib import Path
# from typing import Optional, Dict, Callable, Any
# from functools import partial
#
# from tenacity import retry, stop_after_attempt, wait_exponential
# from loguru import logger
# from langchain_community.document_loaders import UnstructuredImageLoader
# from langchain_core.document_loaders import BaseLoader
#
# from domains.injestion.models import SUPPORTED_FILE_TYPES
#
#
# class ImageProcessingError(Exception):
#     """Custom exception for image processing errors."""
#     pass
#
#
# class ImageLoader:
#     def __init__(self, file_path: str, process_type: str):
#         self.file_path = Path(file_path)
#         self.process_type = process_type
#         self.validate_file()
#
#     def validate_file(self) -> None:
#         """Validate if file exists and has supported extension."""
#         if not self.file_path.exists():
#             raise FileNotFoundError(f"File not found: {self.file_path}")
#
#         if self.file_path.suffix.lower()[1:] not in SUPPORTED_FILE_TYPES:
#             raise ValueError(f"Unsupported file type: {self.file_path.suffix}")
#
#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=1, min=4, max=10),
#         reraise=True
#     )
#     def encode_image_to_base64(self) -> str:
#         """Encode image to base64 with retry mechanism."""
#         try:
#             with open(self.file_path, "rb") as image_file:
#                 return base64.b64encode(image_file.read()).decode('utf-8')
#         except Exception as e:
#             logger.error(f"Error encoding image {self.file_path}: {str(e)}")
#             raise ImageProcessingError(f"Failed to encode image: {str(e)}")
#
#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=1, min=4, max=10),
#         reraise=True
#     )
#     def load_and_encode(self) -> Dict[str, Any]:
#         """Load and encode image with retry mechanism."""
#         try:
#             encoded_image = self.encode_image_to_base64()
#             return {
#                 "content": encoded_image,
#                 "metadata": {
#                     "source": str(self.file_path),
#                     "file_name": self.file_path.name,
#                     "process_type": self.process_type,
#                 }
#             }
#         except Exception as e:
#             logger.error(f"Error processing image {self.file_path}: {str(e)}")
#             raise ImageProcessingError(f"Failed to process image: {str(e)}")
#
#
# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=4, max=10),
#     reraise=True
# )
# def process_image(
#         file_path: str,
#         process_type: str,
# ) -> Dict[str, Any]:
#     """Process image with retry mechanism and proper error handling."""
#     try:
#         loader = ImageLoader(file_path, process_type)
#
#         loaders: Dict[str, Callable[[], BaseLoader]] = {
#             "base64": loader.load_and_encode,
#             "ocr": partial(UnstructuredImageLoader(file_path).load),
#         }
#
#         if process_type not in loaders:
#             raise ValueError(f"Unsupported process type: {process_type}")
#
#         result = loaders[process_type]()
#         logger.info(f"Successfully processed image: {file_path}")
#         return result
#
#     except Exception as e:
#         logger.error(f"Error in process_image for {file_path}: {str(e)}")
#         raise ImageProcessingError(f"Failed to process image: {str(e)}")


import base64
import pprint
import re
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Callable, Any
from functools import partial

from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from langchain_community.document_loaders import UnstructuredImageLoader
from langchain_core.document_loaders import BaseLoader

from domains.injestion.models import SUPPORTED_FILE_TYPES


class ImageProcessingError(Exception):
    """Custom exception for image processing errors."""
    pass


class ImageLoader:
    def __init__(self, file_path: str, process_type: str, image_type: Optional[str] = None):
        self.file_path = Path(file_path)
        self.process_type = process_type
        self.image_type = image_type or self._guess_mime_type()
        self.validate_file()

    def _guess_mime_type(self) -> str:
        """Guess the MIME type of the image file."""
        mime_type, _ = mimetypes.guess_type(self.file_path)
        if not mime_type and self.image_type:
            return "image/jpeg"  # default fallback

        elif self.image_type == "jpg":
            mime_type = "image/jpeg"

        elif self.image_type == "jpeg":
            mime_type = "image/jpeg"

        elif self.image_type == "png":
            mime_type = "image/png"

        elif self.image_type == "gif":
            mime_type = "image/gif"

        elif self.image_type == "webp":
            mime_type = "image/webp"

        logger.debug("Guessed MIME type: %s", mime_type)
        return mime_type

    def validate_file(self) -> None:
        """Validate if file exists and has supported extension."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if self.file_path.suffix.lower()[1:] not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {self.file_path.suffix}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def encode_image_to_base64(self) -> str:
        """Encode image to base64 with retry mechanism."""
        try:
            with open(self.file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image {self.file_path}: {str(e)}")
            raise ImageProcessingError(f"Failed to encode image: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def load_and_encode(self) -> Dict[str, Any]:
        """Load and encode image with retry mechanism."""
        try:
            encoded_image = self.encode_image_to_base64()
            return {
                "content": encoded_image,
                "image_url": f"data:image/{self.image_type};base64,{encoded_image}",
                "metadata": {
                    "source": str(self.file_path),
                    "file_name": self.file_path.name,
                    "process_type": self.process_type,
                    "mime_type": self.image_type
                }
            }

        except Exception as e:
            logger.error(f"Error processing image {self.file_path}: {str(e)}")
            raise ImageProcessingError(f"Failed to process image: {str(e)}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
async def process_image(
        file_path: str,
        process_type: str,
        image_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Process image with retry mechanism and proper error handling."""
    try:
        loader = ImageLoader(file_path, process_type, image_type)

        loaders: Dict[str, Callable[[], BaseLoader]] = {
            "base64": loader.load_and_encode,
            "ocr": partial(UnstructuredImageLoader(file_path).load),
        }

        if process_type not in loaders:
            raise ValueError(f"Unsupported process type: {process_type}")

        result = loaders[process_type]()
        logger.info(f"Successfully processed image: {file_path}")
        return result

    except Exception as e:
        logger.error(f"Error in process_image for {file_path}: {str(e)}")
        raise ImageProcessingError(f"Failed to process image: {str(e)}")


if __name__ == "__main__":
    test_file = "/Users/mohitverma/Downloads/final-image.jpg"
    try:
        # Test base64 encoding
        base64_result = process_image(test_file, "base64", 'jpg')
        logger.info("Base64 encoding successful")
        pprint.pprint(base64_result)

    except ImageProcessingError as e:
        logger.error(f"Processing failed: {str(e)}")