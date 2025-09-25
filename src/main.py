import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from transcribe_yt_video import create_directories, extract_video_id, transcribe_youtube_video, save_transcript
from generate_quiz_from_transcript import generate_quiz_from_transcript, save_raw_open_ai_response
from generate_outputs import clean_raw_quiz_data, export_pdf

# Load in environment variables
load_dotenv()

# Define directories
BASE_DIR = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = BASE_DIR / 'transcripts'
OUTPUTS_DIR = BASE_DIR / 'outputs'
raw_quiz_output_path = BASE_DIR / 'raw_openai'

# Load in API key
API_KEY = os.getenv("OPENAI_API_KEY")

def main(url):
    # Transcribe youtube video and save transcription
    video_id = extract_video_id(url=url)
    raw_transcript = transcribe_youtube_video(video_id=video_id)
    save_transcript(raw=raw_transcript, video_id=video_id)

    # Load in transcription text
    transcript_path = TRANSCRIPTS_DIR / f"{video_id}.txt"
    transcript_text = open(transcript_path).read()

    # Send API call to OpenAI to generate open-ended questions based on the transcription
    # Save the raw quiz output to JSON
    raw_quiz = generate_quiz_from_transcript(transcript_text=transcript_text, api_key=API_KEY)
    save_raw_open_ai_response(response=raw_quiz, video_id=video_id, output_dir=raw_quiz_output_path)

    # Clean raw quiz data and export to pdf
    quiz_data = clean_raw_quiz_data(raw_quiz)
    export_pdf(data=quiz_data, video_id=video_id)