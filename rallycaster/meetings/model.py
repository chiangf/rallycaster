from datetime import datetime

from flask_wtf import Form
from wtforms import validators, TextField, TextAreaField, DateTimeField, FloatField


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

    def get_model_json(self):
        invited_people_list = [invitee.strip() for invitee in self.invited_people.data.split(',')]

        meeting_info = {
            'name': self.name.data,
            'date': self.date.data,
            'invited_people': invited_people_list,
            'description': self.description.data,
            'location': self.location.data,
            'location_latitude': self.location_latitude.data,
            'location_longitude': self.location_longitude.data,
            'created': datetime.utcnow(),
            'updated': datetime.utcnow()
        }

        return meeting_info
