from __future__ import annotations

import time
from threading import Lock
from typing import Any

import requests


class RobotClientError(Exception):
    pass


class RobotClient:
    _instance: 'RobotClient | None' = None
    _lock = Lock()

    def __new__(cls, base_url: str, timeout: float = 2.0, max_retries: int = 3):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, base_url: str, timeout: float = 2.0, max_retries: int = 3):
        if getattr(self, '_initialized', False):
            return
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self._initialized = True

    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            cls._instance = None

    def _request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        url = f'{self.base_url}{endpoint}'
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(method, url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                if response.content:
                    return response.json()
                return {}
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(0.2 * attempt)
        raise RobotClientError(f'Robot API unavailable after retries: {last_error}')

    def get_telemetry(self) -> dict[str, Any]:
        return self._request('GET', '/telemetry')

    def send_command(self, direction: str) -> dict[str, Any]:
        payload = {'direction': direction}
        return self._request('POST', '/move', json=payload)
