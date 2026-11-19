const toast = document.getElementById('toast');
let toastTimer;
function notify(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

// This UI is a front-end demonstration. Connect these actions to your controller API
// before using them to operate real pumps or valves.
const switches = [...document.querySelectorAll('.toggle-switch')];
function setZone(button, enabled, showMessage = true) {
  button.classList.toggle('is-on', enabled);
  button.setAttribute('aria-checked', String(enabled));
  const card = button.closest('.zone-card');
  const status = card.querySelector('.zone-status');
  const stateText = status.querySelector('span');
  status.classList.toggle('running', enabled && button.dataset.zone === 'Garden irrigation');
  status.classList.toggle('idle', !status.classList.contains('running'));
  stateText.textContent = enabled ? (button.dataset.zone === 'Garden irrigation' ? 'Running' : 'Standby') : 'Off';
  const flow = card.querySelector('.zone-flow');
  const previous = Number(flow.textContent);
  flow.textContent = enabled ? (previous > 0 ? previous.toFixed(1) : '4.2') : '0.0';
  const time = card.querySelector('.time-left');
  if (time) time.textContent = enabled && button.dataset.zone === 'Garden irrigation' ? '18 min left' : enabled ? 'On demand' : 'Off';
  if (showMessage) notify(`${button.dataset.zone} ${enabled ? 'turned on' : 'turned off'} · demo mode`);
}
switches.forEach(button => button.addEventListener('click', () => setZone(button, !button.classList.contains('is-on'))));

document.getElementById('allZonesButton').addEventListener('click', event => {
  const allOn = switches.some(button => button.classList.contains('is-on'));
  switches.forEach(button => setZone(button, allOn ? false : true, false));
  event.currentTarget.innerHTML = allOn ? 'Turn all on <span>→</span>' : 'Turn all off <span>→</span>';
  notify(`All zones ${allOn ? 'turned off' : 'turned on'} · demo mode`);
});

document.getElementById('refreshButton').addEventListener('click', event => {
  const button = event.currentTarget;
  button.querySelector('span').style.display = 'inline-block';
  button.querySelector('span').style.animation = 'spin .6s linear';
  setTimeout(() => { button.querySelector('span').style.animation = ''; notify('Dashboard data is up to date.'); }, 650);
});
document.getElementById('chartPeriod').addEventListener('click', () => notify('Showing today’s water flow.'));
document.getElementById('notificationButton').addEventListener('click', () => document.getElementById('alerts').scrollIntoView({behavior:'smooth'}));

const dialog = document.getElementById('scheduleDialog');
document.getElementById('addScheduleButton').addEventListener('click', () => dialog.showModal());
document.getElementById('scheduleForm').addEventListener('submit', event => {
  event.preventDefault();
  const zone = document.getElementById('scheduleZone').value;
  const time = document.getElementById('scheduleTime').value;
  const duration = document.getElementById('scheduleDuration').value;
  const repeat = document.getElementById('scheduleRepeat').value;
  const [hour, minute] = time.split(':').map(Number);
  const displayTime = new Date(2000, 0, 1, hour, minute).toLocaleTimeString([], {hour:'numeric', minute:'2-digit'});
  const days = repeat === 'Weekdays' ? 'MTWTF' : repeat === 'Weekends' ? 'S S' : 'Every day';
  const row = document.createElement('div');
  row.className = 'schedule-row';
  row.innerHTML = `<span class="schedule-icon">◷</span><span class="schedule-info"><b></b><small></small></span><span class="schedule-time"><b></b><small>Upcoming</small></span><span class="schedule-day"></span><span class="schedule-enabled">●</span>`;
  row.querySelector('.schedule-info b').textContent = zone;
  row.querySelector('.schedule-info small').textContent = `Automated · ${duration}`;
  row.querySelector('.schedule-time b').textContent = displayTime;
  row.querySelector('.schedule-day').textContent = days;
  document.getElementById('scheduleList').prepend(row);
  dialog.close();
  event.currentTarget.reset();
  notify(`Schedule added for ${zone} · demo mode`);
});

const menuButton = document.getElementById('menuButton');
menuButton.addEventListener('click', () => document.getElementById('sidebar').classList.toggle('open'));
document.querySelectorAll('.side-nav a').forEach(link => link.addEventListener('click', () => {
  document.querySelectorAll('.side-nav a').forEach(item => item.classList.remove('active'));
  link.classList.add('active');
  document.getElementById('sidebar').classList.remove('open');
}));

const style = document.createElement('style');
style.textContent = '@keyframes spin{to{transform:rotate(360deg)}}';
document.head.appendChild(style);
