import json
from flask import request, current_app
from datetime import datetime, timedelta
from pymongo.cursor import Cursor
from bson import ObjectId


def jsonify_response(status_code=200, *args, **kwargs):
    """
    Variation of https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py
    to support jsonification of Python builtin objects (e.g. datetime).

    Creates a :class:`~flask.Response` with the JSON representation of
    the given arguments with an `application/json` mimetype.  The arguments
    to this function are the same as to the :class:`dict` constructor.

    Example usage::

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify_response(username=g.user.username,
                                    email=g.user.email,
                                    id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }
    """
    json_response = json.dumps(dict(*args, **kwargs),
                               cls=ComplexEncoderToString,
                               indent=None if request.is_xhr else 2)
    response = current_app.response_class(json_response, mimetype='application/json')
    response.status_code = status_code
    return response


def jsonify_js(value):
    """
    Used to serialize objects into json format for jinja2 templates.
    """
    json_value = json.dumps(value, cls=ComplexEncoderToString)
    return json_value


class ComplexEncoderToString(json.JSONEncoder):
    """
    Helps encode JSON object into string even if there are Python datetime or timedelta objects, which
    are normally un-serializable.  Same as ComplexEncoder except datetime and timedelta are converted to strings.

    Usage:
      import json
      serialized_value = json.dumps(value, cls=ComplexEncoderToString)
    """

    def default(self, obj):     # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        elif isinstance(obj, Cursor):
            return [doc for doc in obj]
        else:
            return json.JSONEncoder.default(self, obj)
