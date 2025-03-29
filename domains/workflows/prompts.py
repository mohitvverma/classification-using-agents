# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
#
#
IMAGE_SUMMARY_GENERATION_PROMPT = """
Please provide bullet point summaries for the image in each of the following categories:
- Medium:
- Subject:
- Scene:
- Style:
- Artistic Influence or Movement:
- Website:
- Color:
- Lighting:
- Description:
- Additional Details:

If you don't know the answer for one of the categories, leave it blank."""
#
#
IMAGE_CLASSIFICATION_TEMPLATE = """
Analyze the provided summary of an image and classify whether it contains any of the following categories: offensive content, nudity, or harmful elements. Respond with one of the following labels:

**Image Summary**: {image_summary}

Please classify the image into one of the following categories:
- 'Safe' if the summary does not indicate any of these categories.
- 'Offensive' if the summary suggests offensive content.
- 'Nudity' if the summary suggests the presence of nudity.
- 'Harmful' if the summary suggests harmful content.

Base your classification strictly on the given summary without making any assumptions beyond the provided information.
If the summary is too vague to classify, please respond with 'Unclear' and provide a brief explanation of why you couldn't classify it.

{{
    "classification": classification,
    "explanation": explanation of the classification,
}}
This is a Output JSON object with the following fields:
- image_summary: The summary of the image.
- classification: The classification of the image.
- explanation: An explanation for the classification.
"""
#
#
# def initialize_image_classification_prompt() -> PromptTemplate:
#     """
#     Initialize the image classification prompt template.
#     """
#     return PromptTemplate(
#         input_variables=["image_summary"],
#         template=IMAGE_CLASSIFICATION_TEMPLATE,
#         partial_variables={},
#         validate_template=True,
#         output_parser=JsonOutputParser(),
#     )


from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


# IMAGE_SUMMARY_GENERATION_PROMPT = """Analyze the visible elements in this image and provide factual observations for each category. Use 'Not visible' if a category cannot be determined from the image alone:
#
# 1. Medium: [State the physical or digital medium used]
# 2. Subject: [List primary visible subjects/elements]
# 3. Scene: [Describe the observable setting/environment]
# 4. Style: [Note identifiable artistic or photographic style]
# 5. Color: [List dominant colors present]
# 6. Lighting: [Describe visible lighting conditions]
# 7. Technical Details: [Note any visible technical aspects]
# 8. Composition: [Describe layout and arrangement]
# 9. Key Elements: [List prominent visual features]
# 10. Visual Context: [Describe observable contextual elements]
#
# Provide only information that is directly visible in the image. Do not make assumptions or interpretations."""


# IMAGE_CLASSIFICATION_TEMPLATE = """
# Based solely on the provided image summary, evaluate for content safety using strictly observable elements:
#
# **Image Summary**: {image_summary}
#
# Classification Rules:
# 1. Analyze ONLY the content explicitly mentioned in the summary
# 2. Do not make assumptions about implied content
# 3. Do not consider potential interpretations
# 4. Focus on factual, visible elements
#
# Classify into exactly ONE category:
# - SAFE: Contains no concerning content
# - OFFENSIVE: Contains explicitly offensive elements
# - NUDITY: Contains explicit nudity
# - HARMFUL: Contains elements that could cause harm
# - UNCLEAR: Insufficient information to make determination
#
# Output Format:
# {{
#     "classification": "CATEGORY",
#     "explanation": "Direct evidence from summary that supports classification",
#     "confidence": "HIGH/MEDIUM/LOW based on available information"
# }}
#
# Classify based solely on explicit content in the summary, without inferring or assuming additional context.
# """


def initialize_image_classification_prompt() -> PromptTemplate:
    """
    Initialize the image classification prompt template with strict validation.
    """
    return PromptTemplate(
        input_variables=["image_summary"],
        template=IMAGE_CLASSIFICATION_TEMPLATE,
        partial_variables={},
        validate_template=True,
        output_parser=JsonOutputParser(),
    )