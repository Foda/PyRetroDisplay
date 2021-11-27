import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask


def updateSpotifyStatus() -> dict:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="user-read-playback-state",
        client_id='',
        client_secret='',
        redirect_uri='http://localhost:5000/spotify_callback'))

    results = sp.current_playback()
    current_track = results.get('item') if results else None

    spotify_info = {}
    spotify_info['name'] = current_track.get('name', '') if current_track else ''

    if current_track:
        artist = current_track.get('artists', '')
        if artist and len(artist) > 0:
            spotify_info['artist'] = artist[0].get('name', '')

    return spotify_info


app = Flask(__name__)

@app.route("/spotify")
def spotify_get_info():
    status = updateSpotifyStatus()
    return json.dumps(status)
