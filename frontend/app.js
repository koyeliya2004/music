// Config - change this to your deployed backend URL
const API_URL = 'http://localhost:5000';

let stream = null;

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
    const video = document.getElementById('video');
    video.srcObject = stream;
    video.style.display = 'block';
    document.getElementById('videoOverlay').style.display = 'none';
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('detectBtn').style.display = 'inline-block';
  } catch (err) {
    showError('Camera access denied. Please allow camera permission.');
  }
}

async function detectEmotion() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');

  // Capture frame
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  const imageData = canvas.toDataURL('image/jpeg', 0.8);

  // Show loading
  document.getElementById('cameraSection').classList.add('hidden');
  document.getElementById('loadingSection').classList.remove('hidden');

  // Stop camera
  if (stream) stream.getTracks().forEach(t => t.stop());

  try {
    const response = await fetch(`${API_URL}/detect-emotion`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: imageData })
    });

    if (!response.ok) throw new Error('API error');
    const data = await response.json();

    if (data.error) throw new Error(data.error);

    showResults(data);
  } catch (err) {
    showError(`Detection failed: ${err.message}. Make sure backend is running!`);
  }
}

function showResults(data) {
  document.getElementById('loadingSection').classList.add('hidden');
  document.getElementById('resultSection').classList.remove('hidden');

  // Mood badge
  const badge = document.getElementById('moodBadge');
  badge.textContent = data.mood_label;
  badge.style.background = data.mood_color + '33';
  badge.style.color = data.mood_color;
  badge.style.border = `2px solid ${data.mood_color}`;

  // Emotion bars
  const barsEl = document.getElementById('emotionBars');
  barsEl.innerHTML = '';
  const emotions = data.all_emotions;
  const sorted = Object.entries(emotions).sort((a, b) => b[1] - a[1]);

  sorted.forEach(([emotion, pct]) => {
    const row = document.createElement('div');
    row.className = 'bar-row';
    row.innerHTML = `
      <span class="bar-label">${emotion}</span>
      <div class="bar-track"><div class="bar-fill" data-pct="${pct.toFixed(0)}"></div></div>
      <span class="bar-pct">${pct.toFixed(0)}%</span>
    `;
    barsEl.appendChild(row);
  });

  // Animate bars
  setTimeout(() => {
    document.querySelectorAll('.bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.pct + '%';
    });
  }, 100);

  // Songs
  const grid = document.getElementById('songsGrid');
  grid.innerHTML = '';
  data.songs.forEach(song => {
    const card = document.createElement('a');
    card.className = 'song-card';
    card.href = song.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.innerHTML = `<span class="song-emoji">${song.emoji}</span><span class="song-title">${song.title}</span>`;
    grid.appendChild(card);
  });
}

function showError(msg) {
  document.getElementById('loadingSection').classList.add('hidden');
  document.getElementById('cameraSection').classList.add('hidden');
  document.getElementById('errorSection').classList.remove('hidden');
  document.getElementById('errorMsg').textContent = msg;
}

function resetApp() {
  document.getElementById('resultSection').classList.add('hidden');
  document.getElementById('errorSection').classList.add('hidden');
  document.getElementById('loadingSection').classList.add('hidden');
  document.getElementById('cameraSection').classList.remove('hidden');
  document.getElementById('video').style.display = 'none';
  document.getElementById('videoOverlay').style.display = 'block';
  document.getElementById('startBtn').style.display = 'inline-block';
  document.getElementById('detectBtn').style.display = 'none';
  stream = null;
}
