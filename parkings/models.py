# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from application import db
from common.models import BaseDocument
from mongoengine import CASCADE


class Parking(BaseDocument):
    display_name = db.StringField(
        verbose_name=u'Parking Title',
        max_length=100
    )

    address = db.StringField(
        verbose_name=u'Address',
        max_length=100,
        required=True,
        unique=True
    )

    is_active = db.BooleanField(
        verbose_name=u'Is Active',
        default=True
    )

    meta = {}

    def __unicode__(self):
        return self.display_name


class ParkingSlot(BaseDocument):
    parking_id = db.ReferenceField('Parking', reverse_delete_rule=CASCADE)
    display_name = db.StringField(
        verbose_name=u'Parking Title',
        max_length=100
    )

    meta = {'collection': 'parkingslot'}

    def __unicode__(self):
        return self.display_name


class Booking(BaseDocument):
    user_id = db.ReferenceField('User', reverse_delete_rule=CASCADE)
    parking_id = db.ReferenceField('Parking', reverse_delete_rule=CASCADE)
    parkingslot_id = db.ReferenceField(
        'ParkingSlot', reverse_delete_rule=CASCADE)
    start_time = db.DateTimeField(
        verbose_name=u'Start time',
        required=True
    )
    end_time = db.DateTimeField(
        verbose_name=u'End time',
        required=True
    )
    is_cancelled = db.BooleanField(
        verbose_name=u'Is Cancelled',
        default=False
    )

    meta = {}

    def __unicode__(self):
        return self.start_time + ' ' + self.end_time
