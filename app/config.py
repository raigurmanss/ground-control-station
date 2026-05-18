import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ground_control.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROBOT_API_URL = os.getenv('ROBOT_API_URL', 'http://robot-api:8001')
    ROBOT_TIMEOUT = float(os.getenv('ROBOT_TIMEOUT', '2.0'))
    ROBOT_MAX_RETRIES = int(os.getenv('ROBOT_MAX_RETRIES', '3'))
    TELEMETRY_POLL_SECONDS = float(os.getenv('TELEMETRY_POLL_SECONDS', '2.0'))
    LOW_BATTERY_THRESHOLD = int(os.getenv('LOW_BATTERY_THRESHOLD', '20'))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
