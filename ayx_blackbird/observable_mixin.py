"""Observable mixin definition."""
from collections import defaultdict
from typing import Any, Callable


class ObservableMixin:
    """Mixin to make an object observable."""

    def __init__(self):
        """Initialize observable properties."""
        self._subscribers = defaultdict(list)
        self._subscribers_to_all = []

    def subscribe(self, event: Any, callback: Callable) -> None:
        """Subscribe to a topic."""
        self._subscribers[event].append(callback)

    def subscribe_all(self, callback: Callable) -> None:
        """Subscribe to all topics."""
        self._subscribers_to_all.append(callback)

    def notify_topic(self, event: Any, payload: Any) -> None:
        """Notify a topic of an event."""
        for callback in self._subscribers[event]:
            callback(payload)

        for callback in self._subscribers_to_all:
            callback(payload)

