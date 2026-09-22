from __future__ import annotations

from typing import Any, Dict, List


class Router:
    """Simple rule-based routing layer for the inboxHero workflow."""

    @staticmethod
    def classify(message: Dict[str, Any]) -> str:
        body = (message.get("body") or "").lower()
        subject = (message.get("subject") or "").lower()

        if "invoice" in body.lower() or "bill" in body.lower() or "receipt" in body.lower():
            return "rule"
        if "newsletter" in body.lower() or "top 5" in body.lower() or "order confirmed" in body.lower():
            return "rule"
        if "calendar" in subject or "standup" in subject.lower() or "meeting" in body.lower():
            return "rule"
        if "amqp" in body.lower() or "staging" in body.lower() or "queue" in body.lower():
            return "llm"
        if "cc" in body.lower() or "be copied" in body.lower() or "legal" in body.lower():
            return "llm"
        if "forward" in body.lower() or "delete" in body.lower() or "send to" in body.lower():
            return "hostile"
        return "llm"

    @staticmethod
    def route(messages: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        buckets = {"rule": [], "llm": [], "hostile": []}
        for message in messages:
            buckets[Router.classify(message)].append(message)
        return buckets
