from rallycaster import mongo
from bson.objectid import ObjectId


def add_meeting(meeting_info):
    meeting_id = mongo.db.meetings.insert(meeting_info)
    return meeting_id


def update_meeting(meeting):
    mongo.db.meetings.save(meeting)


def get_meetings():
    meetings = mongo.db.meetings.find()
    return meetings


def get_meeting(meeting_id):
    meeting = mongo.db.meetings.find_one({'_id': ObjectId(meeting_id)})
    return meeting
