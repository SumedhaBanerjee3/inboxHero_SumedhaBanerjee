from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Message:
    id: str
    thread_id: str
    from_email: str
    to: str
    subject: str
    timestamp: str
    body: str
    unread: bool = True

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Message":
        return cls(
            id=payload["id"],
            thread_id=payload["thread_id"],
            from_email=payload["from"],
            to=payload["to"],
            subject=payload["subject"],
            timestamp=payload["timestamp"],
            body=payload["body"],
            unread=payload.get("unread", True),
        )


@dataclass
class Decision:
    message_id: str
    disposition: str
    reason: str
    source: str = "rule"
    cited_ids: List[str] = field(default_factory=list)


@dataclass
class CapabilityResult:
    id: str
    name: str
    status: str
    output: Dict[str, Any]
