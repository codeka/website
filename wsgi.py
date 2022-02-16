from flask import Flask

from ctrl import ctrl, tmpl
from handlers import handlers, blog, snip, main

app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

app.register_blueprint(ctrl)
app.register_blueprint(handlers)

