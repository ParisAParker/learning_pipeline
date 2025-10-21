# config/paths.py
from pathlib import Path

# Base directory (e.g. your project root)
BASE_DIR = Path(__file__).resolve().parents[1]

# Core data directories
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"
PROCESSED_DIR = DATA_DIR / "processed"

# Subdirectories for specific artifacts
TRANSCRIPTS_DIR = RAW_DIR / "transcripts"
METADATA_DIR = INTERMEDIATE_DIR / "metadata"
RAW_OPENAI_DIR = RAW_DIR / "openai_responses"
PROCESSED_OPENAI_DIR = PROCESSED_DIR / "openai_responses"
LOGS_DIR = BASE_DIR / "logs"
PDF_OUTPUTS_DIR =  PROCESSED_DIR/ "pdf_ready"

# Create all directories at import time (optional safety)
for directory in [
    DATA_DIR, RAW_DIR, INTERMEDIATE_DIR, PROCESSED_DIR,
    TRANSCRIPTS_DIR, METADATA_DIR, RAW_OPENAI_DIR,
    LOGS_DIR, PDF_OUTPUTS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)