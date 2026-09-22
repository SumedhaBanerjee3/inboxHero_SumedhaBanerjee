from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_MODEL_STRONG = os.getenv("GEMINI_MODEL_STRONG", "gemini-1.5-pro")

# Gemini is optional for local runs. A real key is only used when the user sets it in .env.
DEFAULT_GEMINI_PLACEHOLDER = "YOUR_GEMINI_API_KEY_HERE"

DATA_PATH = BASE_DIR / "inbox.json"
OUTBOX_DIR = BASE_DIR / "outbox"
TRACE_LOG = BASE_DIR / "trace.jsonl"
PREFERENCES_PATH = BASE_DIR / "prefs.json"


def load_runtime_settings() -> dict:
    """Return the environment configuration used by the agent.

    The API key is intentionally left as a placeholder so the project remains safe
    for a clean checkout without committing secrets.
    """
    return {
        "gemini_api_key": GEMINI_API_KEY,
        "gemini_model": GEMINI_MODEL,
        "gemini_model_strong": GEMINI_MODEL_STRONG,
        "data_path": str(DATA_PATH),
        "outbox_dir": str(OUTBOX_DIR),
        "trace_log": str(TRACE_LOG),
        "preferences_path": str(PREFERENCES_PATH),
    }
