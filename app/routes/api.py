from __future__ import annotations

from functools import wraps

from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required

from ..services.audit_service import AuditService
from ..services.robot_client import RobotClient, RobotClientError
from ..services.telemetry_subject import telemetry_subject


api_bp = Blueprint('api', __name__, url_prefix='/api')


last_known_telemetry: dict = {'battery': None, 'x': 0, 'y': 0, 'status': 'unknown'}
last_connection_state = 'unknown'


def commander_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_commander:
            AuditService.log_event(current_user.username, 'authorization_failure', details={'reason': 'commander role required'}, success=False)
            return jsonify({'error': 'Commander role required'}), 403
        return func(*args, **kwargs)
    return wrapper


def get_robot_client() -> RobotClient:
    return RobotClient(
        current_app.config['ROBOT_API_URL'],
        timeout=current_app.config['ROBOT_TIMEOUT'],
        max_retries=current_app.config['ROBOT_MAX_RETRIES'],
    )


@api_bp.route('/telemetry', methods=['GET'])
@login_required
def telemetry():
    global last_known_telemetry, last_connection_state
    try:
        telemetry_data = get_robot_client().get_telemetry()
        last_known_telemetry = telemetry_data
        last_connection_state = 'connected'
        telemetry_subject.publish(telemetry_data, last_connection_state)
        return jsonify({'telemetry': telemetry_data, 'connection_state': last_connection_state})
    except RobotClientError as exc:
        last_connection_state = 'signal_lost'
        telemetry_subject.publish(last_known_telemetry, last_connection_state)
        return jsonify({
            'telemetry': last_known_telemetry,
            'connection_state': last_connection_state,
            'warning': str(exc),
        }), 200


@api_bp.route('/move', methods=['POST'])
@login_required
@commander_required
def move():
    payload = request.get_json(silent=True) or {}
    direction = payload.get('direction', '').lower()
    if direction not in {'up', 'down', 'left', 'right'}:
        return jsonify({'error': 'Invalid direction'}), 400

    try:
        result = get_robot_client().send_command(direction)
        AuditService.log_event(current_user.username, 'command_sent', command=direction, details=result, success=True)
        return jsonify(result)
    except RobotClientError as exc:
        AuditService.log_event(current_user.username, 'command_failed', command=direction, details={'error': str(exc)}, success=False)
        return jsonify({'error': str(exc)}), 503
