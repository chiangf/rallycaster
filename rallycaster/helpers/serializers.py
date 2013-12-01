import json
from flask import request, current_app
from datetime import datetime, timedelta
from pymongo.cursor import Cursor
from bson import json_util


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
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f%z")   # e.g. 2012-01-20 15:05:02.525389-0500
        elif isinstance(obj, timedelta):
            return str(timedelta)   # TODO: untested
        elif isinstance(obj, Cursor):
            return json_util.dumps(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class ComplexEncoder(json.JSONEncoder):
    """
    Helps encode JSON object into string even if there are Python datetime or timedelta objects, which
    are normally un-serializable.  Same as ComplexEncoderToString except datetime and timedelta are converted
    into a dict with __type__ key.

    Usage:
      import json
      serialized_value = json.dumps(value, cls=ComplexEncoder)
    """

    def default(self, obj):     # pylint: disable=E0202
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
                }
        elif isinstance(obj, timedelta):
            return {
                '__type__': 'timedelta',
                'days': obj.days,
                'seconds': obj.seconds,
                'microseconds': obj.microseconds,
                }
        else:
            return json.JSONEncoder.default(self, obj)


# Disable pylint errors:
#   W0622: Used when a variable or function override a built-in, referring to dict_to_object but this is
#          something that we must override.
#   W0142: Used when a function or method is called using *args or **kwargs to dispatch arguments
# pylint: disable=W0622,W0142
class ComplexDecoder(json.JSONDecoder):
    """
    Helps decode string into JSON object even if there are Python datetime or timedelta objects, which
    are normally un-serializable.  Datetime/timedelta strings must have been encoded by ComplexEncoder,
    this will not work with ComplexEncoderToString or any other type of encoder.

    import json
    Usage: json.loads(str, cls=ComplexDecoder)
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):    # pylint: disable=C0103
        # Return immediately if dict does not have __type__ key
        if '__type__' not in d:
            return d

        value_type = d.pop('__type__')

        if value_type == 'datetime':
            return datetime(**d)
        elif value_type == 'timedelta':
            return timedelta(**d)
        else:
            # Unknown type, leave it the way it was and return
            d['__type__'] = value_type
            return d
