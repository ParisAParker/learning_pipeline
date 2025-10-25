# Base packages
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

# 3rd party packages
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Local modules
from utils.logger import get_logger
from config.paths import TRANSCRIPTS_DIR, METADATA_DIR

logger = get_logger(__name__)

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
    logger.info("Extracting video id from Youtube URL...")

    parsed_url = urlparse(url)
    
    # Case 1: youtu.be/<id>
    if parsed_url.hostname in ["youtu.be"]:
        logger.info("Successfully extracted video id")
        return parsed_url.path[1:]
    
    # Case 2: youtube.com/watch?v=<id>
    if parsed_url.path == "/watch":
        logger.info("Successfully extracted video id")
        return parse_qs(parsed_url.query).get("v", [None])[0]
    
    # Case 3: youtube.com/embed/<id>
    if parsed_url.path.startswith("/embed/"):
        logger.info("Successfully extracted video id")
        return parsed_url.path.split("/")[2]
    
    logger.error("No video id found")
    return None

def transcribe_youtube_video(video_id: str) -> list[dict]:
    """
    Fetches the transcript of a YouTube video and writes it to a text file.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        list[dict]: The raw transcript data, where each entry contains text and timing information
    """
    logger.info("Transcribing Youtube Video...")
    try:
        # Fetch transcript and convert to raw dictionary
        fetched = YouTubeTranscriptApi().fetch(video_id)
        raw = fetched.to_raw_data()
    except Exception as e:
        logger.error(f"Error transcribing video: {str(e)}")
        
    logger.info("Youtube Video Transcribed!")

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

    filepath = TRANSCRIPTS_DIR / f"{video_id}.txt"

    # # Create directory if it doesn't exists
    # if not filepath.exists():
    #     filepath.mkdir(parents=True, exist_ok=True)
    #     logger.info(f"Created directory", filepath)

    # Write to text file
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for entry in raw:
                file.write(entry['text'] + "\n")

            logger.info(f"Transcript saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving Youtube transcript to {filepath}: {e}")
        raise ValueError(str(e))

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

    metadata_filepath = METADATA_DIR / f"{video_id}.json"

    with open(metadata_filepath, 'w') as file:
        json.dump(info, file)
        logger.info(f"Saved metadata to {metadata_filepath}")

def get_yt_video_title_author(video_id: str) -> str:
    metadata_filepath = METADATA_DIR / f"{video_id}.json"

    with open(metadata_filepath, 'r') as file:
        metadata_file = json.load(file)

        video_title = metadata_file['title']
        video_author = metadata_file['channel']

        return video_title, video_author

if __name__ == "__main__":
    video_id = "2_udhlFNNBk"
    result = get_yt_video_title_author(video_id)
    print(result)

## TO DO: Update the all functions that save outputs to new structure (data folder)
## Functions: save_metadata, save transcript