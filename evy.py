import spotipy
from spotipy.oauth2 import SpotifyOAuth

MAX_TRACKS = 500
USER_LIMIT = 50
FEATURES_LIMIT = 100

scope = "user-library-read playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

user_id = sp.me()["id"]

# https://stackoverflow.com/a/312464
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def extract_info(results):
    saved_track_ids = []
    names = []

    for idx, item in enumerate(results["items"]):
        track = item["track"]

        saved_track_ids.append(track["id"])
        names.append(track["name"])

    return saved_track_ids, names

def get_user_library():
    results = sp.current_user_saved_tracks(limit=USER_LIMIT)

    saved_track_ids, names = extract_info(results)

    track_count = USER_LIMIT
    while results['next']:
        results = sp.next(results)

        saved_track_ids_inner, names_inner = extract_info(results)
        saved_track_ids += saved_track_ids_inner
        names += names_inner

        track_count += USER_LIMIT

        if track_count >= MAX_TRACKS:
            return saved_track_ids, names
            
saved_track_ids, names = get_user_library()

saved_track_ids_chunks = chunks(saved_track_ids, 100)

filtered_track_ids = []

for outer_idx, saved_track_ids in enumerate(saved_track_ids_chunks):
    features = sp.audio_features(tracks=saved_track_ids)

    for idx, track in enumerate(features):
        if track["tempo"] >= 120 and track["tempo"] <= 125:
            # print(names[(outer_idx * 50) + idx])
            filtered_track_ids.append(track["id"])

created_playlist_info = sp.user_playlist_create(user=user_id, name="evy running playlist - 120 BPM", public=False)
playlist_id = created_playlist_info["id"]

filtered_track_ids_chunks = chunks(filtered_track_ids, 100)
for idx, filtered_track_ids in enumerate(filtered_track_ids_chunks):
    sp.user_playlist_add_tracks(user_id, playlist_id, filtered_track_ids)
