import requests
from IPython.display import HTML, display

# token = 'BQDPhdevDPvtuHi_6zplGw872JBH3y1NLaFq2o_0_aL_gf7PEXmiofyixGq6E4EeGSS41ndQbGJb-5R9JCOA8YDf8rKU5gvXpWA5OEmYKXyRtr_xIKmmovZ6H_hWtAU7mPUW0YqPUT7ud-VRiTNekONiHN-iR5Z3slo2hf8lLF00husi6vywUwHB_zxXhCri2sEOQDtpAorAdPO_mCNqB5iZOTvJFFLhHOdReRUSnMxn4OXFcCRhZaQCJLaqZzXI0sWMRzOLI2gxPgZqsE4iaCZMn0beN9LtPpabKxpX1_zsjKdgvrWmwOYkYUV2sjjo'
import requests

SPOTIFY_TOKEN = 'BQAIvIk0RMWFWmGp4XyR63nKKv8Bd6eG63QfpDWL42bAn4sgVFwwUKLNK09u_jBJK9rkihMTROkAJ3IFt2igVkhrC81QNYBNcjuymzqsAptMJtH_5R457q_uYH2jugGz5AN_w29hUcJsZ1_9UlXW7I0sVwx7KSKQVYZJUMEixx_jdDB-Ux4A8Cm3OBSgZlLRAfimJgGgGTc4ffZDDkVd0AOkX1BDoU-oRlcq0nCbGFfVUJWx79yuH3_JzWXq0VkkrwO6uddMqlBSeNHBhEEQdR1D8FG8yt6vWHW1ttmUqnVKTmdNfKM7IqiuKwHrz6yd'
 # Replace with a valid token

MOOD_MAP = {
    "POSITIVE": "happy romantic hip hop",
    "NEUTRAL": "love calm chill",
    "NEGATIVE": "motivational workout"
}

def get_songs_by_mood(mood):
    """Returns HTML string with Spotify embeds."""
    query = mood

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}
    params = {"q": query, "type": "track", "limit": 50}

    response = requests.get(url, headers=headers, params=params)
    tracks = response.json().get("tracks", {}).get("items", [])

    if not tracks:
        return "<p>No tracks found.</p>"

    embeds_html = ""
    for track in tracks:
        track_id = track["id"]
        embeds_html += f"""
        <iframe src="https://open.spotify.com/embed/track/{track_id}"
                width="100%" height="80" frameborder="0"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
        </iframe>
        """
    return embeds_html

# print(get_songs_by_mood("arijit singh dhun"))  # Example usage