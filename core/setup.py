from pathlib import Path
from utils.logger import get_logger

BASE_DIR = Path(__file__).resolve().parents[1]
logger = get_logger(__name__)

def create_directories() -> None:
    """Creates directories for each path in dir_paths if they do not already exist"""
    dir_paths = ['data/raw/openai_responses', 'data/raw/transcripts', 'data/intermediate/metadata']

    for path_str in dir_paths:
        path = BASE_DIR / path_str
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info("Created directory:", path)