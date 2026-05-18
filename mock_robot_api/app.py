import random
import time
from flask import Flask, jsonify, request

app = Flask(__name__)
robot_state = {'battery': 100, 'x': 0, 'y': 0, 'status': 'idle'}
GRID_MAX = 9


def maybe_delay_or_fail():
    time.sleep(random.uniform(0.05, 0.5))
    if random.random() < 0.1:
        return jsonify({'error': 'temporary dropout'}), 503
    return None


@app.get('/telemetry')
def telemetry():
    maybe = maybe_delay_or_fail()
    if maybe:
        return maybe
    robot_state['battery'] = max(0, robot_state['battery'] - random.randint(0, 1))
    return jsonify(robot_state)


@app.post('/move')
def move():
    maybe = maybe_delay_or_fail()
    if maybe:
        return maybe

    direction = (request.get_json(silent=True) or {}).get('direction')
    if direction == 'up':
        robot_state['y'] = min(GRID_MAX, robot_state['y'] + 1)
    elif direction == 'down':
        robot_state['y'] = max(0, robot_state['y'] - 1)
    elif direction == 'left':
        robot_state['x'] = max(0, robot_state['x'] - 1)
    elif direction == 'right':
        robot_state['x'] = min(GRID_MAX, robot_state['x'] + 1)
    else:
        return jsonify({'error': 'invalid direction'}), 400
    robot_state['status'] = f'moved_{direction}'
    robot_state['battery'] = max(0, robot_state['battery'] - 1)
    return jsonify({'message': 'movement executed', 'telemetry': robot_state, 'direction': direction})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
