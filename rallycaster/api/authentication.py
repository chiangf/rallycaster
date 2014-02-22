from decorator import decorator
from flask import g, url_for, request, session, redirect

from rallycaster import oauth
from rallycaster.api import api
from rallycaster.api.errors import AuthException
from rallycaster.users import users


SESSION_OAUTH_TYPE = 'oauth_type'
SESSION_OAUTH_TOKEN = 'oauth_token'


class OAuthTokenType(object):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'


def get_user_from_session():
    oauth_type = session.get(SESSION_OAUTH_TYPE)
    oauth_token = session.get(SESSION_OAUTH_TOKEN)

    if None in (oauth_type, oauth_token):
        raise AuthException(u"Invalid or expired session token")

    session_token = oauth_token[0]
    user = users.get_user_by_session_token(session_token)
    if user is None:
        raise AuthException(u"Invalid or expired session token")

    return user


def auth_required():
    @decorator
    def decorated_function(func, *args, **kwargs):
        g.user = get_user_from_session()

        ret = func(*args, **kwargs)
        return ret

    return decorated_function


facebook = oauth.remote_app("facebook", app_key="FACEBOOK")
twitter = oauth.remote_app("twitter", app_key="TWITTER")
google = oauth.remote_app("google", app_key="GOOGLE")


# facebook = oauth.remote_app("facebook",
#                             base_url="https://graph.facebook.com/",
#                             request_token_url=None,
#                             request_token_params={"scope": "publish_stream"},
#                             access_token_url="/oauth/access_token",
#                             authorize_url="https://www.facebook.com/dialog/oauth")
#
# twitter = oauth.remote_app("twitter",
#                            base_url="http://api.twitter.com/1/",
#                            request_token_url="http://api.twitter.com/oauth/request_token",
#                            access_token_url="http://api.twitter.com/oauth/access_token",
#                            authorize_url="http://api.twitter.com/oauth/authenticate")
#
# google = oauth.remote_app("google",
#                           base_url="https://www.google.com/accounts/",
#                           request_token_url=None,
#                           request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email \
#                                                           https://www.googleapis.com/auth/userinfo.profile',
#                                                 'response_type': 'code'},
#                           access_token_url="https://accounts.google.com/o/oauth2/token",
#                           access_token_params={'grant_type': 'authorization_code'},
#                           authorize_url="https://accounts.google.com/o/oauth2/auth")


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get(SESSION_OAUTH_TOKEN)


@api.route('/login/<string:oauth_type>', methods=['GET'])
def login(oauth_type):
    if oauth_type == OAuthTokenType.FACEBOOK:
        response = facebook.authorize(callback=url_for('api.facebook_authorized',
                                      next=request.args.get('next') or request.referrer or None,
                                      _external=True))
    elif oauth_type == OAuthTokenType.GOOGLE:
        response = facebook.authorize(callback=url_for('api.google_authorized',
                                      next=request.args.get('next') or request.referrer or None,
                                      _external=True))
    else:
        raise KeyError(u"Invalid OAuth type")

    return response


@api.route('/login/facebook/authorized/')
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
    user = users.get_user_by_oauth_id(me.data['id'])
    user_info = {
        'first_name': me.data['first_name'],
        'last_name': me.data['last_name'],
        'email': me.data['email'],
        'oauth_id': me.data['id'],
        'oauth_profile_id': me.data['username'],
        'oauth_access_token': response['access_token']
    }

    if user is None:
        users.add_user(user_info)
    else:
        user_info['_id'] = user['_id']
        users.update_user(user_info)

    # Store session token to user id mapping into cache
    users.create_session_for_user(user, session_token)

    return redirect(url_for('frontend.begin'))


@api.route('/login/google/authorized/')
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
    return redirect(url_for('frontend.login'))


@api.route('/logout/', methods=['PUT'])
def logout():
    session.pop(SESSION_OAUTH_TYPE)
    session.pop(SESSION_OAUTH_TOKEN)

    # Raise AuthException so that a 401 error will be thrown and the user will be
    # redirected to the login page.
    raise AuthException(u"Successfully logged out")
