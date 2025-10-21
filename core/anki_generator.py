import requests
from utils.logger import get_logger

logger = get_logger(__name__)

def create_anki_deck(deck_name: str):
    logger.info(f"Creating anki deck named: {deck_name}...")

    requests.post("http://localhost:8765", json={
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    })
    
    logger.info(f"Created anki deck named: {deck_name}")

def generate_anki_cards(deck_name: str, question: str, answer_exp: str, tags: list) -> None:
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

    res = requests.post("http://localhost:8765", json={
        "action": "addNote",
        "version": 6,
        "params": {"note": note}
        })
    
def create_flashcards_from_transcript(deck_name: str, clean_quiz: list) -> None:
    logger.info("Creating Anki Flashcards...")
    
    # Create the new deck name
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