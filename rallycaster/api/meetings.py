from datetime import datetime
from flask import request, Blueprint
from flask_wtf import Form
from wtforms import validators, TextField, TextAreaField, DateTimeField, FloatField
from rallycaster.helpers.serializers import jsonify_response
from rallycaster.api import api
from rallycaster.api.authentication import auth_required
from rallycaster.api.errors import InputException, catch_all
from rallycaster.api.request_callbacks import before_request_callback, after_request_callback
from rallycaster.services import meeting_service


class MeetingForm(Form):
    name = TextField('name', [validators.Length(min=1, max=50)])
    date = DateTimeField('date')
    invited_people = TextField('invited_people')
    description = TextAreaField('description', [validators.Length(min=1, max=1000)])
    location = TextField('location', [validators.Length(min=1, max=500)])
    location_latitude = FloatField('location_latitude', [validators.Optional(),
                                                         validators.NumberRange(min=-90, max=90)])
    location_longitude = FloatField('location_longitude', [validators.Optional(),
                                                           validators.NumberRange(min=-90, max=90)])


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
    meeting_id = meeting_service.add_meeting(meeting_info)

    return jsonify_response(meeting_id=meeting_id)


@api.route('/meetings/<string:meeting_id>', methods=['PUT'])
@auth_required()
def update_meeting(meeting_id):
    form = MeetingForm()
    if not form.validate():
        raise InputException(u"Meeting validation failed")

    meeting = meeting_service.get_meeting(meeting_id)
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

    meeting_service.update_meeting(meeting)

    return jsonify_response(updated=True)


@api.route('/meetings/', methods=['GET'])
@auth_required()
def get_meetings_for_user():
    meetings = meeting_service.get_meetings()
    return jsonify_response(meetings=meetings)
