from pymongo import MongoClient


_client = MongoClient()
_db = _client.rally_database


def add_meeting(meeting_info):
    meeting_id = _db.meetings.insert(meeting_info)
    return meeting_id


def get_meetings():
    meetings = _db.meetings.find()
    return meetings
