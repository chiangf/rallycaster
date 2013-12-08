from decorator import decorator
import requests
import json
from flask import g, url_for, request, session, make_response, render_template, redirect
from flask.ext.oauth import OAuth

from rallycaster import app
from rallycaster.helpers.serializers import jsonify_response
from rallycaster.interfaces.error_handling import AuthException
from rallycaster.services import user_service


SESSION_OAUTH_TYPE = 'oauth_type'
SESSION_OAUTH_TOKEN = 'oauth_token'


class OAuthTokenType(object):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'


def auth_required():
    @decorator
    def decorated_function(func, *args, **kwargs):
        oauth_type = session.get(SESSION_OAUTH_TYPE)
        oauth_token = session.get(SESSION_OAUTH_TOKEN)

        if None in (oauth_type, oauth_token):
            raise AuthException(u"Invalid or expired session token")

        session_token = oauth_token[0]
        user = user_service.get_user_by_session_token(session_token)
        if user is None:
            raise AuthException(u"Invalid or expired session token")

        g.user = user

        ret = func(*args, **kwargs)
        return ret

    return decorated_function


oauth = OAuth()
facebook = oauth.remote_app(app.config['FACEBOOK']['name'],
                            base_url=app.config['FACEBOOK']['base_url'],
                            request_token_url=app.config['FACEBOOK']['request_token_url'],
                            access_token_url=app.config['FACEBOOK']['access_token_url'],
                            authorize_url=app.config['FACEBOOK']['authorize_url'],
                            consumer_key=app.config['FACEBOOK']['consumer_key'],
                            consumer_secret=app.config['FACEBOOK']['consumer_secret'],
                            request_token_params=app.config['FACEBOOK']['request_token_params'])

google = oauth.remote_app(app.config['GOOGLE']['name'],
                          base_url=app.config['GOOGLE']['base_url'],
                          authorize_url=app.config['GOOGLE']['authorize_url'],
                          request_token_url=app.config['GOOGLE']['request_token_url'],
                          request_token_params=app.config['GOOGLE']['request_token_params'],
                          access_token_url=app.config['GOOGLE']['access_token_url'],
                          access_token_params=app.config['GOOGLE']['access_token_params'],
                          consumer_key=app.config['GOOGLE']['consumer_key'],
                          consumer_secret=app.config['GOOGLE']['consumer_secret'])


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get(SESSION_OAUTH_TOKEN)


@app.route('/login/<string:oauth_type>', methods=['GET'])
def login(oauth_type):
    if oauth_type == OAuthTokenType.FACEBOOK:
        response = facebook.authorize(callback=url_for('facebook_authorized',
                                      next=request.args.get('next') or request.referrer or None,
                                      _external=True))
    elif oauth_type == OAuthTokenType.GOOGLE:
        response = facebook.authorize(callback=url_for('google_authorized',
                                      next=request.args.get('next') or request.referrer or None,
                                      _external=True))
    else:
        raise KeyError(u"Invalid OAuth type")

    return response


@app.route('/login/facebook/authorized/')
@facebook.authorized_handler
def facebook_authorized(response):
    if response is None:
        return 'Access denied: reason=%s error=%s' % (request.args['error_reason'],
                                                      request.args['error_description'])

    session_token = response['access_token']
    session[SESSION_OAUTH_TYPE] = OAuthTokenType.FACEBOOK
    session[SESSION_OAUTH_TOKEN] = (session_token, '')

    me = facebook.get('/me')

    # Create user if it does not already exist. If it already exists, update the user information.
    user = user_service.get_user_by_oauth_id(me.data['id'])
    user_info = {
        'first_name': me.data['first_name'],
        'last_name': me.data['last_name'],
        'email': me.data['email'],
        'oauth_id': me.data['id'],
        'oauth_profile_id': me.data['username'],
        'oauth_access_token': response['access_token']
    }

    if user is None:
        user_service.add_user(user_info)
    else:
        user_info['_id'] = user['_id']
        user_service.update_user(user_info)

    # Store session token to user id mapping into cache
    user_service.create_session_for_user(user, session_token)

    return redirect(url_for('begin'))


@app.route('/login/google/authorized/')
@google.authorized_handler
def google_callback(resp):
    # access_token = resp['access_token']
    # session['access_token'] = access_token, ''
    # if access_token:
    #     r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
    #                      headers={'Authorization': 'OAuth ' + access_token})
    #     if r.ok:
    #         data = json.loads(r.text)
    #         oauth_id = data['id']
    #         user = User.load(oauth_id) or User.add(**data)
    #         login_user(user)
    #         next_url = session.get('next') or url_for('index')
    #         return redirect(next_url)
    return redirect(url_for('login'))


@app.route('/logout/', methods=['PUT'])
def logout():
    session.pop(SESSION_OAUTH_TYPE)
    session.pop(SESSION_OAUTH_TOKEN)

    # Raise AuthException so that a 401 error will be thrown and the user will be
    # redirected to the login page.
    raise AuthException(u"Successfully logged out")
