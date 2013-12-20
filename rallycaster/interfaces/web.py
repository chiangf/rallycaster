from decorator import decorator
from flask import render_template, g

from rallycaster import app
from rallycaster.interfaces.authentication import get_user_from_session


@app.route('/', methods=['GET'])
def begin():
    try:
        user = get_user_from_session()
    except:
        user = None

    return render_template('begin.html', user=user)
