import pytest

from app import create_app
from app.services.robot_client import RobotClient


class TestConfig:
    TESTING = True
    SECRET_KEY = 'test-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROBOT_API_URL = 'http://robot-api:8001'
    ROBOT_TIMEOUT = 0.1
    ROBOT_MAX_RETRIES = 1
    LOW_BATTERY_THRESHOLD = 20
    TELEMETRY_POLL_SECONDS = 0.1


@pytest.fixture()
def app():
    RobotClient.reset_instance()
    app = create_app(TestConfig)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
