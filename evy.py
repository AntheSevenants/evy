import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks(limit=50)

saved_track_ids = []

for idx, item in enumerate(results["items"]):
    track = item["track"]
    track_id = track["id"]

    saved_track_ids.append(track_id)

print(saved_track_ids)