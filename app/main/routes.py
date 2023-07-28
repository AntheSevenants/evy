import os
import evy.spotify

from flask import session, redirect, url_for, render_template, request, send_file, current_app, Response
from flask_session import Session
from . import main

@main.route('/')
def index():
    """Renders the landing page

    Returns:
        str: HTML output
    """

    return render_template('index.html')

@main.route('/do', methods = ["GET", "POST"])
def do():
    if request.method == "POST":
        if not "bpm" in request.form:
            return "Malformed POST request."
    
        # Save BPM
        session["bpm"] = request.form["bpm"]
    elif request.method == "GET":
        if not "bpm" in session:
            return "Malformed session."
        
    cache_handler, auth_manager = evy.spotify.get_auth(session)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/do')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = evy.spotify.create_spotipy(auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/playlists">my playlists</a> | ' \
           f'<a href="/currently_playing">currently playing</a> | ' \
        f'<a href="/current_user">me</a>' \

    return render_template('do.html')