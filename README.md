rallycaster
===========

1. Create rallycaster/instance directory and create new rallycaster.cfg file

2. Sample rallycaster.cfg:
```
FACEBOOK = {
    "name": "facebook",
    "base_url": "https://graph.facebook.com/",
    "request_token_url": None,
    "request_token_params": {"scope": "publish_stream"},
    "access_token_url": "/oauth/access_token",
    "authorize_url": "https://www.facebook.com/dialog/oauth",
    "consumer_key": "INSERT CONSUMER KEY",
    "consumer_secret": "INSERT CONSUMER SECRET"
}

TWITTER = {
    "name": "twitter",
    "base_url": "http://api.twitter.com/1/",
    "request_token_url": "http://api.twitter.com/oauth/request_token",
    "access_token_url": "http://api.twitter.com/oauth/access_token",
    "authorize_url": "http://api.twitter.com/oauth/authenticate",
    "consumer_key": "INSERT CONSUMER KEY",
    "consumer_secret": "INSERT CONSUMER SECRET"
}

GOOGLE = {
    "name": "google",
    "base_url": "https://www.google.com/accounts/",
    "request_token_url": None,
    "request_token_params": {'scope': 'https://www.googleapis.com/auth/userinfo.email \
                                       https://www.googleapis.com/auth/userinfo.profile',
                             'response_type': 'code'},
    "access_token_url": "https://accounts.google.com/o/oauth2/token",
    "access_token_params": {'grant_type': 'authorization_code'},
    "authorize_url": "https://accounts.google.com/o/oauth2/auth",
    "consumer_key": "INSERT CONSUMER KEY",
    "consumer_secret": "INSERT CONSUMER SECRET"
}

SECRET_KEY = "INSERT FLASK SECRET KEY"

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DBNAME = "rallydb"

MONGOTEST_HOST = "localhost"
MONGOTEST_PORT = 27017
MONGOTEST_DBNAME = "rallytestdb"

REDIS = {
    "host": "localhost",
    "port": 6379,
    "key_prefix": "rally"
}
```
