import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def create_directories() -> None:
    """Creates directories for each path in dir_paths if they do not already exist"""
    dir_paths = ['transcripts', 'outputs/quizzes', 'outputs/flashcards', 'raw_openai']

    for path_str in dir_paths:
        path = Path(__file__).parent / path_str
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print("Created directory", path)

def extract_video_id(url):
    """
    Extracts the YouTube video ID from a given YouTube URL.

    Supports the following URL formats:
        - youtu.be/<id>
        - youtube.com/watch?v=<id>
        - youtube.com/embed/<id>

    Args:
        url (str): The full YouTube video URL.

    Returns:
        str or None: The extracted video ID if found, otherwise None.
    """
    parsed_url = urlparse(url)
    
    # Case 1: youtu.be/<id>
    if parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    
    # Case 2: youtube.com/watch?v=<id>
    if parsed_url.path == "/watch":
        return parse_qs(parsed_url.query).get("v", [None])[0]
    
    # Case 3: youtube.com/embed/<id>
    if parsed_url.path.startswith("/embed/"):
        return parsed_url.path.split("/")[2]
    
    return None

def transcribe_youtube_video(video_id: str) -> list[dict]:
    """
    Fetches the transcript of a YouTube video and writes it to a text file.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        list[dict]: The raw transcript data, where each entry contains text and timing information
    """
    with st.spinner("Transcribing video..."):
        try:
            # Fetch transcript and convert to raw dictionary
            fetched = YouTubeTranscriptApi().fetch(video_id)
            raw = fetched.to_raw_data()
        except Exception as e:
            st.error(f"Error transcribing video: {str(e)}")
        
    st.success("Video Transcribed!")

    return raw

def save_transcript(raw: list[dict], video_id: str) -> None:

    filepath = Path(__file__).parents[1] / f"transcripts/{video_id}.txt"

    # Write to text file
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in raw:
            f.write(entry['text'] + "\n")

        st.success(f"Transcript saved to: {filepath}")


if __name__ == "__main__":
    video_id = "teCubd25XwI"
    raw = transcribe_youtube_video(video_id)
    save_transcript(raw, video_id)