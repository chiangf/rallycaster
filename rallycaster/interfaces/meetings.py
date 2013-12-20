from datetime import datetime
from flask import request
from rallycaster import app
from rallycaster.helpers.serializers import jsonify_response
from rallycaster.interfaces.authentication import auth_required
from rallycaster.services import meeting_service


@app.route('/meetings/', methods=['POST'])
@auth_required()
def create_meeting():
    meeting_name = request.json['name']
    meeting_date = datetime.strptime(request.json['date'], '%d-%m-%Y')
    meeting_invited_people = request.json['invited_people']
    meeting_description = request.json['description']
    meeting_location = request.json['location']
    meeting_location_latitude = request.json['location_latitude']
    meeting_location_longitude = request.json['location_longitude']

    invited_people = [invitee.strip() for invitee in meeting_invited_people.split(',')]

    meeting_info = {
        'name': meeting_name,
        'date': meeting_date,
        'invited_people': invited_people,
        'description': meeting_description,
        'location': meeting_location,
        'location_latitude': meeting_location_latitude,
        'location_longitude': meeting_location_longitude,
        'created': datetime.utcnow(),
        'updated': datetime.utcnow()
    }
    meeting_id = meeting_service.add_meeting(meeting_info)

    return jsonify_response(meeting_id=meeting_id)


@app.route('/meetings/', methods=['GET'])
@auth_required()
def get_meetings_for_user():
    meetings = meeting_service.get_meetings()
    return jsonify_response(meetings=meetings)
