import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks(limit=50)

saved_track_ids = []
names = []

for idx, item in enumerate(results["items"]):
    track = item["track"]
    track_id = track["id"]
    name = track["name"]

    saved_track_ids.append(track_id)
    names.append(name)

features = sp.audio_features(tracks=saved_track_ids)

for idx, track in enumerate(features):
    if track["tempo"] >= 120 and track["tempo"] <= 125:
        print(names[idx])