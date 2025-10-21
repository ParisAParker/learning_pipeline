import os
from typing import Optional, Dict, Any

from core.pipeline import run_learning_pipeline
from config.variable import OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

def run_app_pipeline(
    youtube_url: Optional[str] = None,
    transcript_text: Optional[str] = None,
    question_count: int = 20,
    input_type: str = "youtube"
) -> Dict[str, Any]:
    """
    Wrapper that loads environment variables, runs pipeline,
    and returns generated artifacts for Streamlit display.
    """

    logger.info("Running app pipeline...")

    result = run_learning_pipeline(
        api_key=OPENAI_API_KEY,
        youtube_url=youtube_url,
        transcript_text=transcript_text,
        question_count=question_count,
        input_type=input_type
    )

    logger.info("Pipeline finished, returning results.")
    return result