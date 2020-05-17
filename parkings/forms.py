# -*- coding: utf-8 -*-
from wtforms import *
from wtforms.fields.html5 import DateTimeLocalField
from flask_wtf import FlaskForm
from flask import g
from parkings.models import Booking, ParkingSlot
from datetime import datetime, timedelta


class ParkingSearchForm(FlaskForm):
    date = DateField(label=u'Select date', default=datetime.utcnow)
    start_time = TimeField(label=u'Select start time',
                           default=datetime.now() + timedelta(hours=1))
    end_time = TimeField(label=u'Select end time',
                         default=datetime.now() + timedelta(hours=2))
    parkingslot_id = HiddenField("Parking slot")

    def save(self):
        parkingslot_id = self.parkingslot_id.data
        parking_id = ParkingSlot.objects.get(pk=parkingslot_id).parking_id.pk
        date = self.date.data
        start_time = datetime.strptime(
            f'{date} {self.start_time.data}', '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(
            f'{date} {self.end_time.data}', '%Y-%m-%d %H:%M:%S')
        user_id = g.user.pk

        booking = Booking(parking_id=parking_id, parkingslot_id=parkingslot_id,
                          start_time=start_time, end_time=end_time, user_id=user_id)
        booking.save()
        return booking
