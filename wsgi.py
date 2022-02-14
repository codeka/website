from flask import Flask

from .ctrl import ctrl, tmpl
from .handlers import handlers, main

app = Flask(__name__)
app.register_blueprint(ctrl)
app.register_blueprint(handlers)

