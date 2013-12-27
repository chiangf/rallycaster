from pymongo import MongoClient
from bson.objectid import ObjectId


_client = MongoClient()
_db = _client.rally_database


def add_meeting(meeting_info):
    meeting_id = _db.meetings.insert(meeting_info)
    return meeting_id


def update_meeting(meeting):
    _db.meetings.save(meeting)


def get_meetings():
    meetings = _db.meetings.find()
    return meetings


def get_meeting(meeting_id):
    meeting = _db.meetings.find_one({'_id': ObjectId(meeting_id)})
    return meeting
