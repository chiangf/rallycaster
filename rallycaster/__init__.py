import logging
from flask import Flask
from flask.ext.pymongo import PyMongo
from flask_wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
from rallycaster.cache import cache


mongo = PyMongo()
csrf = CsrfProtect()
oauth = OAuth()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Turn off strict slashes, which tells Werkzeug to not care about trailing slashes. Thus,
    # hitting /some/url and /some/url/ have the same behavior.
    app.url_map.strict_slashes = False

    app.logger.setLevel(logging.DEBUG)

    # app.config.from_object('rallycaster.default_settings')
    app.config.from_pyfile('rallycaster.cfg')

    mongo.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)
    cache.init_cache(app)

    from rallycaster.api import api, authentication, errors, meetings, request_callbacks
    from rallycaster import frontend
    app.register_blueprint(api)
    app.register_blueprint(frontend.bp)

    from rallycaster import helpers
    app.jinja_env.filters['jsonify_js'] = helpers.serializers.jsonify_js

    return app
