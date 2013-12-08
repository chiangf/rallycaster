from decorator import decorator
from flask import render_template, g

from rallycaster import app
from rallycaster.interfaces.authentication import auth_required


def is_web():
    @decorator
    def decorated_function(func, *args, **kwargs):
        # Indicates that this is an initial web request. E.g., if there's an exception,
        # it should redirect to an error page.
        g.is_web = True

        ret = func(*args, **kwargs)
        return ret

    return decorated_function


@app.route('/')
@is_web()
def index():
    return render_template('login.html')


@app.route('/begin/', methods=['GET'])
@is_web()
@auth_required()
def begin():
    return render_template('begin.html', user=g.user)
