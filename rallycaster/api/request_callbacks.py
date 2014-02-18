from datetime import datetime
from flask import Blueprint, current_app, g, request, render_template_string
from rallycaster.api import api


@api.before_app_request
def before_request_callback(*args, **kwargs):
    g.request_start_time = datetime.utcnow()

    current_app.logger.info(u">>> Start request: {0} {1}".format(request.method, request.path))


@api.after_app_request
def after_request_callback(response):
    elapsed = datetime.utcnow() - g.request_start_time
    current_app.logger.info(u"<<< End request: {0} {1} (elapsed={2} secs)".format(request.method, request.path, elapsed))

    # Enable cross-origin resource sharing (CORS). This will happen in normal EASE admin -> EASE web services
    # calls because this is defined as a cross-origin request. Same origin is defined as
    # same host, same port, and same protocol.
    #
    # We probably want to allow all origins anyways, since we could have API consumers
    # from other origins. All callers still need to authenticate so there shouldn't be any exposed
    # security holes. However, if we nail this down, we can always check if request.headers['Origin']
    # is in a list of hard-coded allowed origins.
    #
    # The problem is that IE only started supporting CORS since IE10 with limited support in IE8,9.
    # We'll need to see just how limited the support is.
    response.headers['Access-Control-Allow-Origin'] = "*"
    if request.method == 'OPTIONS':
        if 'Access-Control-Request-Headers' in request.headers:
            response.headers['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']
        response.headers['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS, PUT, DELETE"

    return response
