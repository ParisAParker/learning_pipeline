import sys
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parents[0] / 'src')
sys.path.append(BASE_DIR)
import streamlit as st
from main import main
from transcribe_yt_video import extract_video_id

st.title("YouTube Transcript Quiz Generator 🎓")

url = st.text_input("Enter a YouTube URL")
video_id = extract_video_id(url)

save_transcript = st.button("Save Transcript")

if url and save_transcript:
    main(url)

# Define saved pdf path
pdf_path = Path(__file__).resolve().parents[0] / f'outputs/quizzes/{video_id}.pdf'

if url:
    # Allow pdf for download in Streamlit
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="Download Quiz PDF",
            data=file,
            file_name="quiz.pdf",
            mime="application/pdf"
        )