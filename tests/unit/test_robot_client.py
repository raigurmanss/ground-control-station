import requests

from app.services.robot_client import RobotClient, RobotClientError


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.content = b'1'

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f'{self.status_code} error')

    def json(self):
        return self._payload


def test_robot_client_retries_and_raises(mocker):
    RobotClient.reset_instance()
    client = RobotClient('http://robot', timeout=0.1, max_retries=2)
    mocker.patch.object(client.session, 'request', side_effect=requests.ConnectionError('boom'))

    try:
        client.get_telemetry()
        assert False, 'Expected RobotClientError'
    except RobotClientError:
        assert True


def test_robot_client_returns_json(mocker):
    RobotClient.reset_instance()
    client = RobotClient('http://robot', timeout=0.1, max_retries=1)
    mocker.patch.object(client.session, 'request', return_value=DummyResponse({'battery': 99, 'x': 2, 'y': 3, 'status': 'idle'}))
    data = client.get_telemetry()
    assert data['battery'] == 99
    assert data['x'] == 2
