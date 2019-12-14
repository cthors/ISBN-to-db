from flask import Flask
from config import Config
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models
