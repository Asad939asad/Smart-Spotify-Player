from flask import Flask, request, jsonify
import os
import pandas as pd
from eeg_to_mood import Final_Prediction
from playlist_generator import get_songs_by_mood
from playlist_for_specificsongs import get_songs_by_mood as get_songs_by_mood_specific
from image_to_mood import predict_single_image
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return open('index.html').read()


@app.route('/mood', methods=['POST'])
def mood():
    data = request.get_json()
    mood_text = data.get("mood", "").strip()

    if not mood_text:
        return "<p>Please enter a mood.</p>", 400

    # Directly fetch songs for the typed mood (no prediction step)
    spotify_html = get_songs_by_mood_specific(mood_text)
    return spotify_html


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        csv_data = pd.read_csv(filepath)
        predictions = Final_Prediction(csv_data)
        mood = predictions[0]

        spotify_html = get_songs_by_mood(mood)
        return spotify_html  # ✅ returns HTML directly

    return 'Invalid file type', 400

# Flask route to handle image uploads
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Class names must match training order
    class_names = ['angry', 'happy', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    # Predict emotion
    predicted_label = predict_single_image(filepath, class_names)

    # Map emotion to Spotify query
    EMOTION_TO_QUERY = {
        'angry': "lo-fi songs",
        'disgust': "romanticsongs",
        'fear': "motivational punjabi songs",
        'happy': "party dance songs",
        'neutral': "acoustic songs",
        'sad': "cheerful songs",
        'surprise': "energetic songs"
    }

    query = EMOTION_TO_QUERY.get(predicted_label,'')
    spotify_html = get_songs_by_mood_specific(query)

    return spotify_html


# def get_songs_by_query(query):
#     """Search Spotify by text query and return embed HTML."""
#     url = "https://api.spotify.com/v1/search"
#     headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}
#     params = {"q": query, "type": "track", "limit": 10}

#     response = requests.get(url, headers=headers, params=params)
#     tracks = response.json().get("tracks", {}).get("items", [])

#     if not tracks:
#         return "<p>No tracks found.</p>"

#     embeds_html = ""
#     for track in tracks:
#         track_id = track["id"]
#         embeds_html += f"""
#         <iframe src="https://open.spotify.com/embed/track/{track_id}"
#                 width="100%" height="80" frameborder="0"
#                 allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
#         </iframe>
#         """
#     return embeds_html

if __name__ == '__main__':
    app.run(debug=True)
