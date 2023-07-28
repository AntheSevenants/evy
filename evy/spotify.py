import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

MAX_TRACKS = os.environ["MAX_TRACKS"]
USER_LIMIT = 50
FEATURES_LIMIT = 100

scope = "user-library-read playlist-modify-private"

def get_auth(session):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = SpotifyOAuth(scope=scope,
                                cache_handler=cache_handler,
                                show_dialog=True)
    
    return cache_handler, auth_manager

def create_spotipy(auth_manager):
    return spotipy.Spotify(auth_manager=auth_manager)

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

def get_user_library(sp):
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
        
def create_playlist(sp, bpm_lower):
    user_id = sp.me()["id"]

    bpm_lower = int(bpm_lower)
    bpm_upper = bpm_lower + 5

    saved_track_ids, names = get_user_library(sp)

    saved_track_ids_chunks = chunks(saved_track_ids, FEATURES_LIMIT)

    filtered_track_ids = []

    for outer_idx, saved_track_ids in enumerate(saved_track_ids_chunks):
        features = sp.audio_features(tracks=saved_track_ids)

        for idx, track in enumerate(features):
            if track["tempo"] >= bpm_lower and track["tempo"] <= bpm_upper:
                filtered_track_ids.append(track["id"])

    filtered_track_count = len(filtered_track_ids)

    # No tracks available
    if filtered_track_count == 0:
        return None, 0

    created_playlist_info = sp.user_playlist_create(user=user_id, name=f"evy running playlist - {bpm_lower} BPM", public=False)
    playlist_id = created_playlist_info["id"]

    filtered_track_ids_chunks = chunks(filtered_track_ids, 100)
    for idx, filtered_track_ids in enumerate(filtered_track_ids_chunks):
        sp.user_playlist_add_tracks(user_id, playlist_id, filtered_track_ids)

    return created_playlist_info["external_urls"]["spotify"], filtered_track_count