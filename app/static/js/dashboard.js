const gridSize = 10;
const gridElement = document.getElementById('grid');
const batteryValue = document.getElementById('batteryValue');
const robotStatus = document.getElementById('robotStatus');
const positionValue = document.getElementById('positionValue');
const connectionBadge = document.getElementById('connectionBadge');
const alertBox = document.getElementById('alertBox');
const commandFeedback = document.getElementById('commandFeedback');
let pollingHandle = null;

function buildGrid() {
  gridElement.innerHTML = '';
  for (let i = 0; i < gridSize * gridSize; i += 1) {
    const cell = document.createElement('div');
    cell.className = 'grid-cell';
    gridElement.appendChild(cell);
  }
}

function updateGrid(x, y) {
  const cells = document.querySelectorAll('.grid-cell');
  cells.forEach((cell) => cell.classList.remove('robot'));
  const row = gridSize - 1 - Math.max(0, Math.min(gridSize - 1, y));
  const col = Math.max(0, Math.min(gridSize - 1, x));
  const index = row * gridSize + col;
  if (cells[index]) {
    cells[index].classList.add('robot');
  }
}

function setConnectionState(state) {
  connectionBadge.textContent = state.replace('_', ' ');
  connectionBadge.className = `status-badge ${state}`;
}

function setAlert(message, level='warning') {
  if (!message) {
    alertBox.className = 'alert hidden';
    alertBox.textContent = '';
    return;
  }
  alertBox.className = `alert ${level}`;
  alertBox.textContent = message;
}

async function fetchTelemetry() {
  try {
    setConnectionState('reconnecting');
    const response = await fetch('/api/telemetry');
    const data = await response.json();
    const telemetry = data.telemetry || {};
    setConnectionState(data.connection_state || 'unknown');
    batteryValue.textContent = telemetry.battery ?? '--';
    robotStatus.textContent = telemetry.status ?? '--';
    positionValue.textContent = `(${telemetry.x ?? 0}, ${telemetry.y ?? 0})`;
    updateGrid(telemetry.x ?? 0, telemetry.y ?? 0);

    if ((telemetry.battery ?? 100) <= window.dashboardConfig.lowBatteryThreshold) {
      setAlert(`Low battery alert: ${telemetry.battery}% remaining`, 'warning');
    } else if (data.connection_state === 'signal_lost') {
      setAlert('Signal lost. Displaying last known telemetry while backend retries the robot connection.', 'danger');
    } else {
      setAlert('');
    }
  } catch (error) {
    setConnectionState('signal_lost');
    setAlert('Dashboard could not reach the server. Retrying automatically...', 'danger');
  }
}

async function sendMove(direction) {
  commandFeedback.textContent = 'Sending command...';
  try {
    const response = await fetch('/api/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ direction }),
    });
    const data = await response.json();
    if (!response.ok) {
      commandFeedback.textContent = data.error || 'Command failed.';
      return;
    }
    commandFeedback.textContent = `Command '${direction}' executed successfully.`;
    await fetchTelemetry();
  } catch (error) {
    commandFeedback.textContent = 'Command failed due to network/server error.';
  }
}

function startPolling() {
  if (pollingHandle) clearInterval(pollingHandle);
  fetchTelemetry();
  pollingHandle = setInterval(fetchTelemetry, window.dashboardConfig.pollSeconds * 1000);
}

buildGrid();
startPolling();

document.querySelectorAll('.move-btn').forEach((button) => {
  button.addEventListener('click', () => sendMove(button.dataset.direction));
});
