import os
import argparse
from app import create_app

parser = argparse.ArgumentParser(description='Run frontend')
parser.add_argument('-debug', '--debug', nargs='?', type=bool, default=False, help='whether to run in debug mode')

args = parser.parse_args()

debug = args.debug

environment_variables = [ "SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI", "MAX_TRACKS" ]

for environment_variable in environment_variables:
	if not environment_variable in os.environ:
		raise Exception(f"Environment variable '{environment_variable}' missing")

app = create_app(debug=debug)

if debug:
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', debug=debug)
else:
	from waitress import serve
	print("evy frontend started")
	serve(app, host='0.0.0.0', port=8080)