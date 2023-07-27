import os
import argparse
from app import create_app

parser = argparse.ArgumentParser(description='Run frontend')
parser.add_argument('-debug', '--debug', nargs='?', type=bool, default=False, help='whether to run in debug mode')

args = parser.parse_args()

debug = args.debug

app = create_app(debug=debug)

if debug:
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', debug=debug)
else:
	from waitress import serve
	print("evy frontend started")
	serve(app, host='0.0.0.0', port=8080)