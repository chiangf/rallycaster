from datetime import datetime

from rallycaster import helpers
from rallycaster import mongo


class UserService(object):
    def get_user_by_id(self, user_id):
        user = mongo.db.users.find_one({'_id': user_id})
        return user

    def get_user_by_oauth_id(self, oauth_id):
        user = mongo.db.users.find_one({'oauth_id': oauth_id})
        return user

    def add_user(self, user_info):
        user_id = mongo.db.users.insert(user_info)
        return user_id

    def update_user(self, user_info):
        mongo.db.users.update({'_id': user_info['_id']}, user_info, upsert=False)

    def create_session_for_user(self, user, session_token):
        session_info = {
            'user_id': user['_id'],
            'token': session_token,
            'created': datetime.utcnow()
        }
        mongo.db.sessions.insert(session_info)

        session_token = helpers.session.generate_guid()
        return session_token

    def get_user_by_session_token(self, session_token):
        session = mongo.db.sessions.find_one({'token': session_token})
        user_id = session['user_id']

        user = self.get_user_by_id(user_id)
        return user
