import os

from flask import session, redirect, url_for, render_template, request, send_file, current_app, Response
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
    if request.method != "POST":
        return "This endpoint only accepts POST requests."
    
    if not "bpm" in request.form:
        return "Malformed POST request."

    return render_template('do.html')