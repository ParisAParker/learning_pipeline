import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANKI_CONNECT_URL = "http://host.docker.internal:8765"

## TODO:
# Configure the AnkiConnect URL so it'll run successfully locally or in a docker container