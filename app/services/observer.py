"""Lightweight Observer pattern — emit events, listeners react."""

from collections import defaultdict
from typing import Any, Callable

EventListener = Callable[[dict[str, Any]], None]

_listeners: dict[str, list[EventListener]] = defaultdict(list)


def on(event: str, listener: EventListener) -> None:
    """Register a listener for an event type."""
    _listeners[event].append(listener)


def emit(event: str, data: dict[str, Any] | None = None) -> None:
    """Fire all listeners registered for *event*."""
    for listener in _listeners.get(event, []):
        listener(data or {})


def clear() -> None:
    """Remove all listeners (useful in tests)."""
    _listeners.clear()
