from flask import Blueprint, current_app, render_template
from flask_login import current_user, login_required

from ..models import MissionLog


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    recent_logs = MissionLog.query.order_by(MissionLog.timestamp.desc()).limit(20).all()
    return render_template(
        'dashboard.html',
        user=current_user,
        low_battery_threshold=current_app.config['LOW_BATTERY_THRESHOLD'],
        poll_seconds=current_app.config['TELEMETRY_POLL_SECONDS'],
        recent_logs=recent_logs,
    )
