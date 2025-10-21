import os
import json
import streamlit as st
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
from transcribe_yt_video import create_directories, extract_video_id, transcribe_youtube_video, save_transcript, save_metadata
from generate_quiz_from_transcript import generate_quiz_from_transcript, save_raw_open_ai_response
from generate_outputs import clean_raw_quiz_data, export_pdf, create_flashcards_from_transcript
from send_email import send_email

# Load in environment variables
load_dotenv()

# Define directories
BASE_DIR = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = BASE_DIR / 'transcripts'
OUTPUTS_DIR = BASE_DIR / 'outputs'
raw_quiz_output_path = BASE_DIR / 'raw_openai'

# Load in API key
API_KEY = os.getenv("OPENAI_API_KEY")

def main(youtube: bool, question_count: int, url: Optional[str] = None, transcript_text: Optional[str] = None, deck_name: Optional[str]=None, transcript_id: Optional[str]=None):
    if youtube == True:
        # Transcribe youtube video and save transcription
        video_id = extract_video_id(url=url)
        raw_transcript = transcribe_youtube_video(video_id=video_id)
        save_metadata(url=url, video_id=video_id)
        save_transcript(raw=raw_transcript, video_id=video_id)

        # Load in transcription text
        transcript_path = TRANSCRIPTS_DIR / f"{video_id}.txt"
        transcript_text = open(transcript_path).read()

        # Send API call to OpenAI to generate open-ended questions based on the transcription
        # Save the raw quiz output to JSON
        raw_quiz = generate_quiz_from_transcript(transcript_text=transcript_text, api_key=API_KEY, question_count=question_count)
        save_raw_open_ai_response(response=raw_quiz, video_id=video_id, output_dir=raw_quiz_output_path)

        # Clean raw quiz data and export to pdf
        raw_quiz_dict_path = raw_quiz_output_path / f"{video_id}.json"
        with open(raw_quiz_dict_path, "rb") as file:
            raw_quiz_dict = json.load(file)

        quiz_data = clean_raw_quiz_data(raw_quiz_dict)
    else:
        raw_quiz = generate_quiz_from_transcript(transcript_text=transcript_text, api_key=API_KEY, question_count=question_count)
        save_raw_open_ai_response(response=raw_quiz, video_id=transcript_id, output_dir=raw_quiz_output_path)
        
        # Clean raw quiz data and export to pdf
        raw_quiz_dict_path = raw_quiz_output_path / f"{transcript_id}.json"
        with open(raw_quiz_dict_path, "rb") as file:
            raw_quiz_dict = json.load(file)

        quiz_data = clean_raw_quiz_data(raw_quiz_dict)

    # If youtube is true, thn the deck name should be channel_name::video_title
    if youtube == True:
        # Open metadata file
        METADATA_DIR = Path(__file__).resolve().parents[1] / 'metadata'
        metadata_filepath = METADATA_DIR / f"{video_id}.json"
        with open(metadata_filepath, 'r') as file:
            metadata = json.load(file) 

        # Create a deck and sub-deck for Anki using channel name and video title respectively       
        video_title = metadata['title']
        channel_name = metadata['channel']
        deck_name = channel_name + "::" + video_title

        # Create Anki Flashcards
        create_flashcards_from_transcript(deck_name=deck_name, clean_quiz=quiz_data)
    else:
        create_flashcards_from_transcript(deck_name=deck_name, clean_quiz=quiz_data)

    if youtube == True:
        export_pdf(data=quiz_data, video_id=video_id)
        send_email(transcript_id=transcript_id)
    else:
        export_pdf(data=quiz_data, video_id=transcript_id)
        send_email(transcript_id=transcript_id)



if __name__ == "__main__":
    print("Hello")

# Code Review Feedback
# ✅ Strengths:
# The code is structured clearly and readable.
# You’ve modularized functionality (imported helpers like transcribe_youtube_video, generate_quiz_from_transcript, etc.).
# You’re using pathlib (👍 modern standard) and .env files for API keys (👍 security).
# Variable names are meaningful (video_id, raw_quiz_output_path, etc.).

# ⚙️ Areas to improve:
# Your main() is doing too much — it contains business logic, flow control, and file I/O all in one place.
# There’s no error handling, meaning one failed API call or missing file will crash the run.
# You have duplicate code between the YouTube and text branches.
# There’s no logging, so debugging will be hard at scale.
# The function and file boundaries aren’t clearly enforced — e.g., main.py both orchestrates and executes transformations.jj