from typing import Optional

import requests

from utils.logger import get_logger

logger = get_logger(__name__)

def create_anki_deck(deck_name: str):
    logger.info(f"Creating anki deck named: {deck_name}...")

    try:
        requests.post("http://localhost:8765", json={
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name}
        })    
        logger.info(f"Created anki deck named: {deck_name}")
    except Exception as e:
        logger.warning(f"Error creating deck_name: {deck_name}")
        logger.warning("Could not reach AnkiConnect on port 8765.")
        logger.warning("Please open Anki Desktop and ensure the AnkiConnect plugin is installed and enabled")

def generate_anki_cards(
        deck_name: str, 
        question: str, 
        answer_exp: str, 
        tags: list
    ) -> None:
    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": f"{question}",
            "Back": f"{answer_exp}"
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": tags
    }

    try:
        requests.post("http://localhost:8765", json={
            "action": "addNote",
            "version": 6,
            "params": {"note": note}
            })
    except Exception as e:
        logger.warning("Error generating anki cards")
        logger.warning("Could not reach AnkiConnect on port 8765.")
        logger.warning("Please open Anki Desktop and ensure the AnkiConnect plugin is installed and enabled")
    
def create_flashcards_from_transcript(
        clean_quiz: list,
        user_deck_name: Optional[str] = None, 
        video_title: Optional[str] = None,
        channel_name: Optional[str] = None
    ) -> None:
    logger.info("Creating Anki Flashcards...")
    
    if video_title and channel_name:
        deck_name = f"{channel_name}::{video_title}"         
        # Create the new deck name
        create_anki_deck(deck_name)
    else:
        deck_name = user_deck_name.copy()
        create_anki_deck(deck_name)

    logger.info("Generating Anki Flashcards...")
    # Add all the cards to the deck
    for content in clean_quiz:
        question = content['question']
        answer_exp = content['answer'] + " Explanation: " + content['explanation']
        tags = []

        generate_anki_cards(
            deck_name=deck_name,
            question=question,
            answer_exp=answer_exp,
            tags=tags
            )
    logger.info("Finished generating Anki Flashcards")