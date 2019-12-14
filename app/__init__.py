from flask import Flask
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

from app import routes
