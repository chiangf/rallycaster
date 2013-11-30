from flask import url_for, request, session, make_response, render_template
from flask.ext.oauth import OAuth
from rallycaster import app
from rallycaster.services import user_service


oauth = OAuth()

#twitter = oauth.remote_app('twitter',
#                           base_url='http://api.twitter.com/1/',
#                           request_token_url='http://api.twitter.com/oauth/request_token',
#                           access_token_url='http://api.twitter.com/oauth/access_token',
#                           authorize_url='http://api.twitter.com/oauth/authenticate',
#                           consumer_key='JXq2DU8wtU9xq5VDTnxTWw',
#                           consumer_secret='RmQrLDnCqSoOzrtwSY3VdhxerqpH1EZTpHTHU9XS0'
#)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="257720404339505",
    consumer_secret="2426fb4a30eabf79f915d1d39f5b3570",
    request_token_params={'scope': 'publish_stream'}
)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/login')
def login():
    print(url_for('facebook_authorized'))

    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
            )
    session['oauth_token'] = (resp['access_token'], '')
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
            'oauth_access_token': resp['access_token']
        }
        user_service.add_user(user)

    # Store session token to user id mapping into cache
    session_token = user_service.create_session_for_user(user)

    response = make_response(render_template('index.html', user=user))
    response.set_cookie('session-token', session_token)

    return response
