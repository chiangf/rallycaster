from datetime import datetime
from bson import json_util
from flask import request
from rallycaster import app
from rallycaster.helpers.serializers import jsonify_response
from rallycaster.services import meeting_service


@app.route('/meetings', methods=['POST'])
def create_meeting():
    # TODO: remove me
    asdf = json_util.loads(request.form)

    meeting_name = request.form['meeting_name']
    meeting_date = datetime.strptime(request.form['meeting_date'], '%d-%m-%Y')
    meeting_description = request.form['meeting_description']
    meeting_location = request.form['meeting_location']
    meeting_loc_latitude = request.form['meeting_loc_latitude']
    meeting_loc_longitude = request.form['meeting_loc_longitude']

    meeting_info = {
        'name': meeting_name,
        'date': meeting_date,
        'description': meeting_description,
        'location': meeting_location,
        'location_latitude': meeting_loc_latitude,
        'location_longitude': meeting_loc_longitude,
        'created': datetime.utcnow(),
        'updated': datetime.utcnow()
    }
    meeting_id = meeting_service.add_meeting(meeting_info)

    return jsonify_response(meeting_id=meeting_id)


@app.route('/meetings', methods=['GET'])
def get_meetings_for_user():
    meetings = meeting_service.get_meetings()
    return jsonify_response(meetings=meetings)
