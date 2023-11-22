import sys, os

# Ensure this path is writable by the user the WSGI daemon runs as
os.environ['OGD_FLASK_APP_LOG_FILE'] = '/var/log/flask-apps/data-app.log'

if not "DEPLOY_PATH" in sys.path:
    sys.path.append("DEPLOY_PATH")
    sys.path.append("DEPLOY_PATH/opengamedata")
os.chdir("DEPLOY_PATH")
from data_app import application