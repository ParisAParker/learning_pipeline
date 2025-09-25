import os
import streamlit as st
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# # Load environment variables
# load_dotenv()

# # Load in transcript
# transcript_path = Path.cwd().parent / 'transcripts/teCubd25XwI.txt'
# transcript_text = open(transcript_path).read()

def generate_quiz_from_transcript(transcript_text: str, api_key: str) -> str:
    """
    Generates quiz questions and answers from a transcript using the OpenAI API.

    Args:
        transcript_text (str): The transcript text to base the quiz on.
        api_key (str): Your OpenAI API key.

    Returns:
        str: The raw response from the OpenAI API, typically a JSON-formatted string containing quiz questions, answers, and explanations.
    """

    # Create prompt to generate quiz
    prompt = f"""
    You are an expert quiz generator.

    I will give you a transcript. Based ONLY on that transcript:

    1. Generate 20 well-written **open-ended questions**.  
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

    Here is the transcript:
    ---
    {transcript_text}
    """
    with st.spinner("Generating raw quiz..."):
        try:
            # Generate quiz from OpenAI's gpt-4o model
            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7  # controls creativity
            )
        except Exception as e:
            st.error(f"Error generating quiz: {str(e)}")
    
    st.success("Generated raw quiz!")

    return response


def save_raw_open_ai_response(response: str, video_id: str, output_dir: str) -> None:
    """
    Saves the raw OpenAI API response to a file for a given video ID.

    Args:
        response (dict): The raw response data from the OpenAI API.
        video_id (str): The YouTube video ID associated with the response.
        output_dir (str): The directory path where the response file will be saved.

    Returns:
        None
    """

    with st.spinner("Saving raw quiz JSON..."):
        try:
            # Save raw open AI response to dictionary
            response_dict = response.to_dict()
            response_dict['video_id'] = video_id

            output_path = output_dir / f"{video_id}.json"

            # Save JSON to raw location
            with open(output_path, 'w') as file:
                json.dump(response_dict, file)
        except Exception as e:
            st.error(f"Error saving raw quiz JSON: {str(e)}")

    st.success(f"Saved raw quiz JSON to: {output_dir}")


        