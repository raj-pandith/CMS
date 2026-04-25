"""
The flask application package.
"""
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__, template_folder='FlaskWebProject/templates')
app.config.from_object(Config)
app.logger.setLevel(logging.DEBUG)

# Set up detailed logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)  # Changed from WARNING to DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
app.logger.addHandler(streamHandler)

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Add error logging handler
@app.errorhandler(Exception)
def log_exception(e):
    app.logger.exception(f"Unhandled exception: {str(e)}")
    raise

import FlaskWebProject.views
