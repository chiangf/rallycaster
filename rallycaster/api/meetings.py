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

    invited_people_list = [invitee.strip() for invitee in form.invited_people.data.split(',')]

    meeting_info = {
        'name': form.name.data,
        'date': form.date.data,
        'invited_people': invited_people_list,
        'description': form.description.data,
        'location': form.location.data,
        'location_latitude': form.location_latitude.data,
        'location_longitude': form.location_longitude.data,
        'created': datetime.utcnow(),
        'updated': datetime.utcnow()
    }
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

    invited_people_list = [invitee.strip() for invitee in form.invited_people.data.split(',')]

    meeting['name'] = form.name.data
    meeting['date'] = form.date.data
    meeting['invited_people'] = invited_people_list
    meeting['description'] = form.description.data
    meeting['location'] = form.location.data
    meeting['location_latitude'] = form.location_latitude.data
    meeting['location_longitude'] = form.location_longitude.data
    meeting['updated'] = datetime.utcnow()

    meetings.update_meeting(meeting)

    return jsonify_response(updated=True)


@api.route('/meetings/', methods=['GET'])
@auth_required()
def get_meetings_for_user():
    meetings_for_user = meetings.get_meetings()
    return jsonify_response(meetings=meetings_for_user)
