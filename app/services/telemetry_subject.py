from __future__ import annotations

from typing import Any

from .audit_service import AuditService
from .observer import Observer, Subject


class TelemetryAuditObserver(Observer):
    def update(self, payload: dict[str, Any], connection_state: str) -> None:
        AuditService.log_telemetry(payload, connection_state)


class TelemetrySubject(Subject):
    def publish(self, payload: dict[str, Any], connection_state: str) -> None:
        self.notify(payload, connection_state)


telemetry_subject = TelemetrySubject()
telemetry_subject.attach(TelemetryAuditObserver())
