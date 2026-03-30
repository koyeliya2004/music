from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
from deepface import DeepFace
import os

app = Flask(__name__)
CORS(app)

# Mood to YouTube search query mapping
MOOD_MUSIC = {
    "happy": {
        "label": "Happy 😄",
        "color": "#FFD700",
        "songs": [
            {"title": "Happy - Pharrell Williams", "url": "https://www.youtube.com/results?search_query=Happy+Pharrell+Williams", "emoji": "🎵"},
            {"title": "Can't Stop the Feeling - Justin Timberlake", "url": "https://www.youtube.com/results?search_query=Can't+Stop+the+Feeling+Justin+Timberlake", "emoji": "🎶"},
            {"title": "Uptown Funk - Bruno Mars", "url": "https://www.youtube.com/results?search_query=Uptown+Funk+Bruno+Mars", "emoji": "🎸"},
            {"title": "Good as Hell - Lizzo", "url": "https://www.youtube.com/results?search_query=Good+as+Hell+Lizzo", "emoji": "🎤"},
            {"title": "Walking on Sunshine", "url": "https://www.youtube.com/results?search_query=Walking+on+Sunshine+Katrina+Waves", "emoji": "☀️"}
        ]
    },
    "sad": {
        "label": "Sad 😢",
        "color": "#6495ED",
        "songs": [
            {"title": "Someone Like You - Adele", "url": "https://www.youtube.com/results?search_query=Someone+Like+You+Adele", "emoji": "💙"},
            {"title": "Fix You - Coldplay", "url": "https://www.youtube.com/results?search_query=Fix+You+Coldplay", "emoji": "🎵"},
            {"title": "The Night We Met - Lord Huron", "url": "https://www.youtube.com/results?search_query=The+Night+We+Met+Lord+Huron", "emoji": "🌙"},
            {"title": "Skinny Love - Bon Iver", "url": "https://www.youtube.com/results?search_query=Skinny+Love+Bon+Iver", "emoji": "🍂"},
            {"title": "Arijit Singh Sad Songs", "url": "https://www.youtube.com/results?search_query=Arijit+Singh+sad+songs", "emoji": "🎶"}
        ]
    },
    "angry": {
        "label": "Angry 😠",
        "color": "#FF4500",
        "songs": [
            {"title": "Lose Yourself - Eminem", "url": "https://www.youtube.com/results?search_query=Lose+Yourself+Eminem", "emoji": "🔥"},
            {"title": "Break Stuff - Limp Bizkit", "url": "https://www.youtube.com/results?search_query=Break+Stuff+Limp+Bizkit", "emoji": "💢"},
            {"title": "In The End - Linkin Park", "url": "https://www.youtube.com/results?search_query=In+The+End+Linkin+Park", "emoji": "⚡"},
            {"title": "Killing in the Name - RATM", "url": "https://www.youtube.com/results?search_query=Killing+in+the+Name+RATM", "emoji": "🎸"},
            {"title": "Numb - Linkin Park", "url": "https://www.youtube.com/results?search_query=Numb+Linkin+Park", "emoji": "🤘"}
        ]
    },
    "surprise": {
        "label": "Surprised 😮",
        "color": "#FF69B4",
        "songs": [
            {"title": "Wow - Post Malone", "url": "https://www.youtube.com/results?search_query=Wow+Post+Malone", "emoji": "✨"},
            {"title": "Shape of You - Ed Sheeran", "url": "https://www.youtube.com/results?search_query=Shape+of+You+Ed+Sheeran", "emoji": "🎵"},
            {"title": "Blinding Lights - The Weeknd", "url": "https://www.youtube.com/results?search_query=Blinding+Lights+The+Weeknd", "emoji": "💡"},
            {"title": "Levitating - Dua Lipa", "url": "https://www.youtube.com/results?search_query=Levitating+Dua+Lipa", "emoji": "🚀"},
            {"title": "Dynamite - BTS", "url": "https://www.youtube.com/results?search_query=Dynamite+BTS", "emoji": "💥"}
        ]
    },
    "fear": {
        "label": "Fearful 😨",
        "color": "#9370DB",
        "songs": [
            {"title": "Thriller - Michael Jackson", "url": "https://www.youtube.com/results?search_query=Thriller+Michael+Jackson", "emoji": "👻"},
            {"title": "Disturbed - Sound of Silence", "url": "https://www.youtube.com/results?search_query=Sound+of+Silence+Disturbed", "emoji": "🌑"},
            {"title": "Breathe - Flyleaf", "url": "https://www.youtube.com/results?search_query=Breathe+Flyleaf", "emoji": "🎵"},
            {"title": "Evanescence - My Immortal", "url": "https://www.youtube.com/results?search_query=My+Immortal+Evanescence", "emoji": "🖤"},
            {"title": "Imagine Dragons - Demons", "url": "https://www.youtube.com/results?search_query=Demons+Imagine+Dragons", "emoji": "🌊"}
        ]
    },
    "disgust": {
        "label": "Disgusted 🤢",
        "color": "#3CB371",
        "songs": [
            {"title": "Radioactive - Imagine Dragons", "url": "https://www.youtube.com/results?search_query=Radioactive+Imagine+Dragons", "emoji": "☢️"},
            {"title": "Toxicity - System of a Down", "url": "https://www.youtube.com/results?search_query=Toxicity+System+of+a+Down", "emoji": "💀"},
            {"title": "Smells Like Teen Spirit - Nirvana", "url": "https://www.youtube.com/results?search_query=Smells+Like+Teen+Spirit+Nirvana", "emoji": "🎸"},
            {"title": "Black Hole Sun - Soundgarden", "url": "https://www.youtube.com/results?search_query=Black+Hole+Sun+Soundgarden", "emoji": "🌑"},
            {"title": "Deftones - Change", "url": "https://www.youtube.com/results?search_query=Change+Deftones", "emoji": "🎵"}
        ]
    },
    "neutral": {
        "label": "Neutral 😐",
        "color": "#708090",
        "songs": [
            {"title": "Lofi Hip Hop Radio", "url": "https://www.youtube.com/results?search_query=lofi+hip+hop+radio", "emoji": "🎧"},
            {"title": "Chill Vibes Playlist", "url": "https://www.youtube.com/results?search_query=chill+vibes+playlist", "emoji": "😌"},
            {"title": "Study Music - Deep Focus", "url": "https://www.youtube.com/results?search_query=study+music+deep+focus", "emoji": "📚"},
            {"title": "Coldplay - Yellow", "url": "https://www.youtube.com/results?search_query=Yellow+Coldplay", "emoji": "🌟"},
            {"title": "Indie Chill Mix", "url": "https://www.youtube.com/results?search_query=indie+chill+mix", "emoji": "🎶"}
        ]
    }
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Mood Music API is running 🎵", "endpoints": ["/detect-emotion", "/songs/<emotion>"]})

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Decode base64 image
        img_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        img_bytes = base64.b64decode(img_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image'}), 400

        # Use DeepFace to analyze emotion (pretrained model)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]

        dominant_emotion = result['dominant_emotion'].lower()
        all_emotions = result['emotion']

        # Map to our mood keys
        emotion_map = {
            'happy': 'happy', 'sad': 'sad', 'angry': 'angry',
            'surprise': 'surprise', 'fear': 'fear',
            'disgust': 'disgust', 'neutral': 'neutral'
        }
        mood_key = emotion_map.get(dominant_emotion, 'neutral')
        mood_data = MOOD_MUSIC[mood_key]

        return jsonify({
            'emotion': dominant_emotion,
            'mood_key': mood_key,
            'mood_label': mood_data['label'],
            'mood_color': mood_data['color'],
            'all_emotions': all_emotions,
            'songs': mood_data['songs']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/songs/<emotion>', methods=['GET'])
def get_songs(emotion):
    emotion = emotion.lower()
    if emotion in MOOD_MUSIC:
        return jsonify(MOOD_MUSIC[emotion])
    return jsonify({'error': 'Emotion not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
