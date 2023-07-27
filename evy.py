import spotipy
from spotipy.oauth2 import SpotifyOAuth

MAX_LOOPS = 10

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

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
    results = sp.current_user_saved_tracks(limit=50)

    saved_track_ids, names = extract_info(results)

    loops = 0
    while results['next']:
        results = sp.next(results)

        saved_track_ids_inner, names_inner = extract_info(results)
        saved_track_ids += saved_track_ids_inner
        names += names_inner

        loops += 1

        if loops >= MAX_LOOPS:
            return saved_track_ids, names
            
saved_track_ids, names = get_user_library()

saved_track_ids_chunks = chunks(saved_track_ids, 50)

for outer_idx, saved_track_ids in enumerate(saved_track_ids_chunks):
    features = sp.audio_features(tracks=saved_track_ids)

    for idx, track in enumerate(features):
        if track["tempo"] >= 120 and track["tempo"] <= 125:
            print(names[(outer_idx * 50) + idx])