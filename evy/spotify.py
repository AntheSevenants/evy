import spotipy
from spotipy.oauth2 import SpotifyOAuth

MAX_TRACKS = 500
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