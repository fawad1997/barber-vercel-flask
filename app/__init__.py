from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import logging

app = Flask(__name__)
app.config.from_object(Config)
#
# # Configure login manager
# login_manager = LoginManager()
# login_manager.init_app(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# Setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')