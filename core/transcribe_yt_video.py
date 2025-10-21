import json
import yt_dlp
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path
from urllib.parse import urlparse, parse_qs



def extract_video_id(url: str) -> None:
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
    """
    Save a YouTube transcript to a text file.

    Each transcript entry is expected to be a dictionary with a 'text' key.
    The transcript will be written line by line into a file located in the
    `transcripts/` directory, named after the given video ID.

    Args:
        raw (list[dict]): A list of transcript entries, each containing a 'text' field.
        video_id (str): The YouTube video ID used to name the output file.

    Returns:
        None
    """

    filepath = Path(__file__).parents[1] / f"transcripts/{video_id}.txt"

    # Write to text file
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in raw:
            f.write(entry['text'] + "\n")

        st.success(f"Transcript saved to: {filepath}")

def save_metadata(url: str, video_id: str) -> None:
    """
    Extract and save metadata for a YouTube video.

    Uses yt-dlp to fetch metadata (without downloading the video)
    and saves it as a JSON file in the `metadata/` directory, named
    after the given video ID.

    Args:
        url (str): The full YouTube video URL.
        video_id (str): The YouTube video ID used to name the output file.

    Returns:
        None
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    metadata_filepath = str(Path(__file__).resolve().parents[1] / f'metadata/{video_id}.json')

    with open(metadata_filepath, 'w') as file:
        json.dump(info, file)


if __name__ == "__main__":
    video_id = "teCubd25XwI"
    raw = transcribe_youtube_video(video_id)
    save_transcript(raw, video_id)

## TO DO: Update the all functions that save outputs to new structure (data folder)
## Functions: save_metadata, save transcript