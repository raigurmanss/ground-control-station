from app.extensions import db
from app.models import MissionLog, User


class FakeRobotClient:
    def get_telemetry(self):
        return {'battery': 90, 'x': 1, 'y': 2, 'status': 'idle'}

    def send_command(self, direction: str):
        return {'message': 'ok', 'direction': direction}


class FailingRobotClient:
    def get_telemetry(self):
        raise Exception('unreachable')


def register_and_login(client, username='alice', role='commander'):
    client.post('/register', data={
        'username': username,
        'email': f'{username}@example.com',
        'password': 'secret123',
        'role': role,
    }, follow_redirects=True)
    client.post('/login', data={'username': username, 'password': 'secret123'}, follow_redirects=True)


def test_dashboard_requires_auth(client):
    response = client.get('/')
    assert response.status_code in {301, 302}


def test_commander_can_move_robot(client, app, mocker):
    register_and_login(client, role='commander')
    mocker.patch('app.routes.api.get_robot_client', return_value=FakeRobotClient())
    response = client.post('/api/move', json={'direction': 'up'})
    assert response.status_code == 200
    with app.app_context():
        assert MissionLog.query.count() == 1


def test_viewer_cannot_move_robot(client, app):
    register_and_login(client, username='viewer1', role='viewer')
    response = client.post('/api/move', json={'direction': 'up'})
    assert response.status_code == 403


def test_telemetry_endpoint_returns_data(client, mocker):
    register_and_login(client, role='viewer')
    mocker.patch('app.routes.api.get_robot_client', return_value=FakeRobotClient())
    response = client.get('/api/telemetry')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['telemetry']['x'] == 1
