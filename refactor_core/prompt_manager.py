from utils.logger import get_logger

logger = get_logger(__name__)

def build_quiz_prompt(transcript_text: str, num_questions: int = 20) -> str:
    """Build a formatted prompt for the OpenAI model"""
    # Create prompt to generate quiz
    prompt = f"""
    You are an expert quiz generator.

    I will give you a transcript. Based ONLY on that transcript:

    1. Generate {str(num_questions)} well-written **open-ended questions**.  
    - Each question should test reasoning, application, or connections across ideas, not just recall.  
    - Provide a strong sample answer with a short explanation of why it is correct.  

    2. Return your output in **JSON** with the following structure:
    [
    {{
        "question": "string",
        "answer": "string",
        "explanation": "string"
    }},
    ...
    ]

    Transcript:
    ---
    {transcript_text}
    """
    logger.info("Built prompt")
    return prompt.strip()