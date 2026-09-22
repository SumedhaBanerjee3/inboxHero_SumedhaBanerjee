from __future__ import annotations

import os
from typing import Any, Optional

from config import DEFAULT_GEMINI_PLACEHOLDER, GEMINI_API_KEY, GEMINI_MODEL


class GeminiClient:
    """Small wrapper over the Gemini SDK with a safe fallback for local runs."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or GEMINI_MODEL or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self._model: Any = None
        self._genai: Any = None
        self._init()

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key != DEFAULT_GEMINI_PLACEHOLDER and self.api_key.strip())

    def _init(self) -> None:
        if not self.is_configured():
            return
        try:
            import google.generativeai as genai  # type: ignore
        except Exception:
            return

        self._genai = genai
        self._genai.configure(api_key=self.api_key)
        self._model = self._genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        if not self.is_configured() or self._model is None:
            raise RuntimeError("Gemini is not configured. Set GEMINI_API_KEY in .env to enable model calls.")

        response = self._model.generate_content(prompt)
        try:
            return response.text
        except Exception:
            if hasattr(response, "candidates"):
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    return "".join(part.text for part in candidate.content.parts if hasattr(part, "text"))
            raise

    def safe_generate(self, prompt: str, fallback: str = "") -> str:
        if not self.is_configured():
            return fallback
        try:
            result = self.generate(prompt)
            return result.strip() or fallback
        except Exception:
            return fallback
