from decorator import decorator
from flask import g, url_for, request, session, make_response, render_template, redirect
from flask.ext.oauth import OAuth
from rallycaster import app
from rallycaster.interfaces.error_handling import AuthException
from rallycaster.services import user_service


def auth_required():
    @decorator
    def decorated_function(func, *args, **kwargs):
        oauth_token = session.get('oauth_token')
        if oauth_token is None:
            raise AuthException(u"Session token not found")

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
                            request_token_params=app.config['FACEBOOK']['request_token_params']
)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@app.route('/login/authorized/oauth')
@facebook.authorized_handler
def facebook_authorized(response):
    if response is None:
        return 'Access denied: reason=%s error=%s' % (request.args['error_reason'],
                                                      request.args['error_description'])

    session_token = response['access_token']
    session['oauth_token'] = (session_token, '')

    me = facebook.get('/me')

    # Create user if it does not already exist
    user = user_service.get_user_by_oauth_id(me.data['id'])

    if user is None:
        user = {
            'first_name': me.data['first_name'],
            'last_name': me.data['last_name'],
            'email': me.data['email'],
            'oauth_id': me.data['id'],
            'oauth_profile_id': me.data['username'],
            'oauth_access_token': response['access_token']
        }
        user_service.add_user(user)

    # Store session token to user id mapping into cache
    session_token = response['access_token']
    user_service.create_session_for_user(user, session_token, is_oauth=True)

    return redirect(url_for('index'))
