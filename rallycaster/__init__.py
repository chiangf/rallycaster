from flask import Flask
app = Flask(__name__, instance_relative_config=True)

from rallycaster import config
config.set_configuration()

from flask.ext.pymongo import PyMongo
from flask_wtf.csrf import CsrfProtect
mongo = PyMongo(app)
csrf = CsrfProtect(app)

import interfaces.request_callbacks
import interfaces.error_handling
import interfaces.web
import interfaces.authentication
import interfaces.meetings

from rallycaster import helpers
app.jinja_env.filters['jsonify_js'] = helpers.serializers.jsonify_js
