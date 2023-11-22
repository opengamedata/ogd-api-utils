import sys
import os

# Ensure this path is writable by the user the WSGI daemon runs as
os.environ['OGD_FLASK_APP_LOG_FILE'] = '/var/log/flask-apps/codes-app.log'

if not "DEPLOY_PATH" in sys.path:
    sys.path.append("DEPLOY_PATH")
from codes_app import application
