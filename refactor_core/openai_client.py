# Base libraries
import time
from datetime import datetime
import json
from pathlib import Path
from typing import Optional

# 3rd party libraries
from openai import OpenAI

# Local modules
from utils.logger import get_logger

logger = get_logger(__name__)

def call_openai_api(
        api_key: str,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
    """
    Send a prompt to OpenAI and return the response text
    """
    client = OpenAI(api_key=api_key)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Sending request to OpenAI...")
            response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature  # controls creativity
            )
            logger.info(f"OpenAI response received successfully on attempt {attempt}")
            return response
        
        except Exception as e:
            logger.warning(f"OpenAI call failed (attempt {attempt}): {e}")
            time.sleep(2 * attempt) # exponential backoff
    


def save_raw_open_ai_response(
        response, 
        output_dir: str,
        source_id: Optional[str]=None, 
        input_type: str = "text"
    ) -> None:
    """
    Save the raw OpenAI API response (including metadata) to disk.

    Args:
        response: The OpenAI response object (supports .to_dict()).
        output_dir (str | Path): Directory where the file should be saved.
        source_id (str, optional): A unique identifier for the input source
                                   (e.g., YouTube video ID or filename stem).
        input_type (str): Type of input source. Defaults to 'text'.

    Returns:
        Path: Path to the saved JSON file.
    """

    # Normalize and ensure directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a unique timestamped name
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    base_name = source_id or f"{input_type}_{timestamp}"
    output_path = output_dir / f"{base_name}.json"

    # Add metadata and convert to dict
    try:
        response_dict = response.to_dict() if hasattr(response, "to_dict") else response
        response_dict["metadata"] = {
            "source_id": source_id,
            "input_type": input_type,
            "timestamp": timestamp,
        }

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(response_dict, file, indent=2)

        logger.info(f"Saved OpenAI response for {input_type} → {output_path}")
        return output_path

    except Exception as e:
        logger.exception(f"Failed to save OpenAI response: {e}")