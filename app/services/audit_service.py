import json
from typing import Any

from ..extensions import db
from ..models import MissionLog, TelemetrySnapshot


class AuditService:
    @staticmethod
    def log_event(username: str, event_type: str, command: str | None = None, details: dict[str, Any] | None = None, success: bool = True) -> None:
        entry = MissionLog(
            username=username,
            event_type=event_type,
            command=command,
            details=json.dumps(details or {}),
            success=success,
        )
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def log_telemetry(telemetry: dict[str, Any], connection_state: str) -> None:
        snapshot = TelemetrySnapshot(
            battery=telemetry.get('battery'),
            x=telemetry.get('x'),
            y=telemetry.get('y'),
            status=telemetry.get('status'),
            connection_state=connection_state,
        )
        db.session.add(snapshot)
        db.session.commit()
