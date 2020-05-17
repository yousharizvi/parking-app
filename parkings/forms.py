# -*- coding: utf-8 -*-
from wtforms import *
from flask_wtf import FlaskForm
from flask_mail import Message

from application import mail
from accounts.models import User


class ParkingCreateForm(FlaskForm):

    display_name = TextField(
        label=u'Parking Name',
        validators=[
            validators.required()
        ]
    )

    address = TextField(
        label=u'Address',
        validators=[
            validators.required()
        ]
    )

    next = HiddenField()


class ParkingSlotCreateForm(FlaskForm):

    display_name = TextField(
        label=u'Parking Name',
        validators=[
            validators.required()
        ]
    )

    parking_id = SelectField(u'Parking',
        [validators.required()],
        choices=[(r._id, r.display_name) for r in Parking.objects],
        coerce=int)

    next = HiddenField()
