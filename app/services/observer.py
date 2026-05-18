from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Lock
from typing import Any


class Observer(ABC):
    @abstractmethod
    def update(self, payload: dict[str, Any], connection_state: str) -> None:
        raise NotImplementedError


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._lock = Lock()

    def attach(self, observer: Observer) -> None:
        with self._lock:
            self._observers.append(observer)

    def notify(self, payload: dict[str, Any], connection_state: str) -> None:
        with self._lock:
            observers = list(self._observers)
        for observer in observers:
            observer.update(payload, connection_state)
