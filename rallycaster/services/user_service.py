from datetime import datetime

from pymongo import MongoClient

from rallycaster.helpers import session


_client = MongoClient()
_db = _client.rally_database


def get_user_by_oauth_id(oauth_id):
    user = _db.users.find_one({'oauth_id': oauth_id})
    return user


def add_user(user_info):
    user_id = _db.users.insert(user_info)
    return user_id


def create_session_for_user(user):
    session_token = session.generate_guid()

    session_info = {
        'user_id': user['_id'],
        'token': session_token,
        'created': datetime.utcnow()
    }
    _db.sessions.insert(session_info)

    return session_token
