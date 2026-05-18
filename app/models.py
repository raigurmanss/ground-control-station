from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_commander(self) -> bool:
        return self.role == 'commander'


class MissionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    command = db.Column(db.String(50), nullable=True)
    details = db.Column(db.Text, nullable=True)
    success = db.Column(db.Boolean, default=True, nullable=False)


class TelemetrySnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    battery = db.Column(db.Integer, nullable=True)
    x = db.Column(db.Integer, nullable=True)
    y = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    connection_state = db.Column(db.String(30), nullable=False, default='unknown')


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
