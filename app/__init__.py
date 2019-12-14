from flask import Flask
from config import Config
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.config.from_object(Config)

from app import routes
