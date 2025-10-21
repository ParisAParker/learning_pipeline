import json
from pathlib import Path
from utils.logger import get_logger
from config.paths import PROCESSED_DIR

logger = get_logger(__name__)

def extract_quiz_content(response_dict: dict, source_id: str):
    """Extract the quiz content from OpenAI's response"""
    try:
        output = response_dict['choices'][0]['message']['content']

        
        if "```json" in output:
            json_output = output.split("```json")[1].split("```")[0].strip()
        else:
            logger.error("JSON block not found")
            raise ValueError("JSON block not found")

        # Try to parse JSON, log and raise clean error if invalid
        try:
            data = json.loads(json_output)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON content: {e}")
            logger.debug(f"Raw content was: \n{json_output[:500]}")
            raise ValueError("OpenAI response did not contain valid JSON") from e
        
        save_parsed_quiz(
            data = data,
            output_path = PROCESSED_DIR / f"{source_id}.json"
        )

        logger.info(f"Successfully extracted {len(data)} quiz items from response.")
        return data

    except Exception as e:
        logger.exception(f"Error extracting quiz content: {e}")
        raise ValueError(f"Error extracting quiz content: {e}")

def save_parsed_quiz(data: dict, output_path: Path) -> None:
    """
    Save parsed and validated quiz JSON to disk.
    """
    # Where am I saving the processed quiz
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Clean quiz JSON saved to {output_path}")