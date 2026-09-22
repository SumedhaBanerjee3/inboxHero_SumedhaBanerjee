from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class PreferenceStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = {}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def set_preference(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def clear(self) -> None:
        self.data = {}
        self.save()
