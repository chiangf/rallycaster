from flask import Blueprint, render_template
from rallycaster.api.authentication import get_user_from_session


bp = Blueprint('frontend', __name__, static_folder='static', template_folder='templates')


@bp.route('/', methods=['GET'])
def begin():
    try:
        user = get_user_from_session()
    except:
        user = None

    return render_template('begin.html', user=user)
