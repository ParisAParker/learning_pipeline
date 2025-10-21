import sys
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parents[0] / 'src')
sys.path.append(BASE_DIR)
import streamlit as st
from main import main
from transcribe_yt_video import extract_video_id

st.title("YouTube Transcript Quiz Generator 🎓")

# User chooses source
source = st.radio(
    "Choose input method:",
    ["YouTube URL", "Upload Transcript JSON"]
)

if source == 'YouTube URL':
    youtube = True

    question_count = st.number_input(
    "Enter number of questions",
    min_value=5, 
    max_value=20,
    value=10,       
    step=1   
    )

    url = st.text_input("Enter a YouTube URL")
    video_id = extract_video_id(url)

    save_transcript = st.button("Generate Quiz")

    if url and save_transcript:
        main(youtube=youtube, question_count=question_count, url=url)

    # Define saved pdf path
    pdf_path = Path(__file__).resolve().parents[0] / f'outputs/quizzes/{video_id}.pdf'

    if pdf_path.exists():
        # Allow pdf for download in Streamlit
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download Quiz PDF",
                data=file,
                file_name="quiz.pdf",
                mime="application/pdf"
            )

elif source == "Upload Transcript JSON":
    youtube = False
    
    question_count = st.number_input(
    "Enter number of questions",
    min_value=5, 
    max_value=20,
    value=10,       
    step=1   
    )   

    uploaded_file = st.file_uploader("Choose a text file", type=['txt'])

    if uploaded_file is not None:
        content = uploaded_file.read()

        transcript_id = st.text_input("Enter a unique name/ID for this transcript (no spaces)", value="my_transcript")

        # Deck name input
        deck_name = st.text_input("Enter deck name (e.g., Subject or Category)", value="MyDeck")

        # Sub-deck option
        use_subdeck = st.radio("Do you want a sub-deck?", ["No", "Yes"])

        subdeck = ""
        if use_subdeck == "Yes":
            subdeck = st.text_input("Enter sub-deck name (e.g., Lesson 1)")

        # Construct final deck
        final_deck = f"{deck_name}::{subdeck}" if subdeck else deck_name
        st.info(f"Final deck will be: **{final_deck}**")

        generate_quiz = st.button("Generate Quiz")

        if generate_quiz:
            main(youtube=youtube, question_count=question_count, transcript_text=content, deck_name=final_deck, transcript_id=transcript_id)


