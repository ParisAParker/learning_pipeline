
# Standard library
import json
from pathlib import Path
from typing import Optional, Dict, Any
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Third-party
import streamlit as st
from dotenv import load_dotenv

# Local modules
from utils.logger import get_logger
from config.paths import TRANSCRIPTS_DIR, RAW_OPENAI_DIR
from config.variable import OPENAI_API_KEY
from setup import create_directories
from transcript_service import (
    extract_video_id,
    transcribe_youtube_video, 
    save_transcript, 
    save_metadata
)
from prompt_manager import build_quiz_prompt
from openai_client import (
    call_openai_api,
    save_raw_open_ai_response
)
from parser import (
    extract_quiz_content
)
from pdf_generator import export_pdf
from anki_generator import create_flashcards_from_transcript

logger = get_logger(__name__)

def run_learning_pipeline(
    api_key: str,
    youtube_url: Optional[str] = None,
    transcript_text: Optional[str] = None,
    question_count: int = 20,
    input_type: str = "youtube"
) -> Dict[str, Any]:
    """
    Core orchestration function for generating quizzes and outputs.
    This function contains no Streamlit logic.
    """

    logger.info(f"Starting learning pipeline. Input type: {input_type}")

    # 1. SETUP
    create_directories()
    load_dotenv()

    # 2. INGEST TRANSCRIPT
    logger.info("Ingesting Transcript...")

    if input_type == "youtube":
        video_id = extract_video_id(youtube_url)
        raw_transcript = transcribe_youtube_video(video_id)
        save_transcript(raw_transcript, video_id)
        save_metadata(youtube_url, video_id)
        transcript_text = (TRANSCRIPTS_DIR / f"{video_id}.txt").read_text()
        source_id = video_id
    else:
        source_id = f"text_{Path.cwd().stem}"
    
    logger.info("Ingested Transcript")

    # 3. BUILD PROMPT
    prompt = build_quiz_prompt(transcript_text, question_count)

    # 4. CALL OPENAI
    response = call_openai_api(api_key=api_key, prompt=prompt)
    save_raw_open_ai_response(
        response=response, 
        output_dir = RAW_OPENAI_DIR,
        source_id=source_id
    )

    # 5. PARSE & VALIDATE
    quiz_data = extract_quiz_content(response.to_dict(), source_id)

    # 6. GENERATE OUTPUTS
    export_pdf(quiz_data, source_id)
    create_flashcards_from_transcript(deck_name=source_id, clean_quiz=quiz_data)

    logger.info("✅ Learning pipeline completed successfully.")
    return {"source_id": source_id, "quiz_data": quiz_data}

if __name__ == "__main__":
    response = run_learning_pipeline(
        api_key = OPENAI_API_KEY,
        youtube_url= "https://www.youtube.com/watch?v=2UvHiH7zJLU",
    )
    print(response)