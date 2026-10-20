import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://127.0.0.1:11434/v1"

TEST_IDENTITIES = {
    "alice": {
        "token": "alice-token",
        "user_id": 1,
        "role": "user",
    },
    "bob": {
        "token": "bob-token",
        "user_id": 2,
        "role": "user",
    },
    "admin": {
        "token": "admin-token",
        "user_id": 3,
        "role": "admin",
    },
}