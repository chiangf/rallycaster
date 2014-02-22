from bson.objectid import ObjectId
from rallycaster import mongo


class MeetingService(object):
    def add_meeting(self, meeting_info):
        meeting_id = mongo.db.meetings.insert(meeting_info)
        return meeting_id

    def update_meeting(self, meeting):
        mongo.db.meetings.save(meeting)

    def get_meetings(self):
        meetings = mongo.db.meetings.find()
        return meetings

    def get_meeting(self, meeting_id):
        meeting = mongo.db.meetings.find_one({'_id': ObjectId(meeting_id)})
        return meeting
