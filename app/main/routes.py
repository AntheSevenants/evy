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