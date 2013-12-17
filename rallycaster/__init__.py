from flask import Flask
app = Flask(__name__, instance_relative_config=True)

from config import config
config.set_configuration()

import interfaces.request_callbacks
import interfaces.error_handling
import interfaces.web
import interfaces.authentication
import interfaces.meetings

from rallycaster.helpers import serializers
app.jinja_env.filters['jsonify_js'] = serializers.jsonify_js
