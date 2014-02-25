from datetime import datetime

from rallycaster.helpers.serializers import jsonify_response
from rallycaster.api import api
from rallycaster.api.authentication import auth_required
from rallycaster.api.errors import InputException
from rallycaster.meetings import meetings, MeetingForm


@api.route('/meetings/', methods=['POST'])
@auth_required()
def create_meeting():
    form = MeetingForm()
    if not form.validate():
        raise InputException(u"Meeting validation failed")

    meeting_info = form.get_model_json()
    meeting_id = meetings.add_meeting(meeting_info)

    return jsonify_response(meeting_id=meeting_id)


@api.route('/meetings/<string:meeting_id>', methods=['PUT'])
@auth_required()
def update_meeting(meeting_id):
    form = MeetingForm()
    if not form.validate():
        raise InputException(u"Meeting validation failed")

    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        raise InputException(u"Meeting {0} does not exist".format(meeting_id))

    updated_meeting_info = form.get_model_json()

    for key, value in meeting.iteritems():
        if not key.startswith('_'):
            meeting[key] = updated_meeting_info[key]

    meetings.update_meeting(meeting)

    return jsonify_response(updated=True)


@api.route('/meetings/', methods=['GET'])
@auth_required()
def get_meetings_for_user():
    meetings_for_user = meetings.get_meetings()
    return jsonify_response(meetings=meetings_for_user)
