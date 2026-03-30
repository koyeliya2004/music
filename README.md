# 🎵 MoodTunes - Mood-Based Music Recommender

A full-stack web app that detects your facial emotion using AI and recommends YouTube music based on your mood!

## ✨ Features
- 📸 Real-time webcam face emotion detection
- 🤖 Powered by **DeepFace** pretrained model (no training needed!)
- 🎶 Recommends 5 songs per mood (Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral)
- 📊 Shows emotion probability bars
- 🎨 Beautiful animated dark UI
- 🔗 Clickable links to YouTube search

## 🗂️ Project Structure
```
music/
├── backend/
│   ├── app.py           # Flask API
│   ├── requirements.txt # Python dependencies
│   └── Procfile         # For Render deployment
├── frontend/
│   ├── index.html       # Main UI
│   ├── style.css        # Styling
│   └── app.js           # Frontend logic
└── README.md
```

## 🚀 How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs at: `http://localhost:5000`

### Frontend
Open `frontend/index.html` in your browser directly, OR use Live Server in VS Code.

> Make sure `API_URL` in `app.js` points to your backend URL.

## ☁️ Deploy
- **Backend** → Deploy on [Render](https://render.com) (free)
- **Frontend** → Deploy on [GitHub Pages](https://pages.github.com) or [Netlify](https://netlify.com)

After deploying backend, update `API_URL` in `frontend/app.js` to your Render URL.

## 🎭 Supported Moods
| Emotion | Songs Type |
|---------|------------|
| 😄 Happy | Upbeat, energetic |
| 😢 Sad | Emotional, slow |
| 😠 Angry | Rock, rap |
| 😮 Surprise | Pop, trending |
| 😨 Fear | Dark, intense |
| 🤢 Disgust | Alternative, grunge |
| 😐 Neutral | Lofi, chill |

## 👩‍💻 Made by
**Koyeliya Ghosh** - MAKAUT CSE 5th Sem
