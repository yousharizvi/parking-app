# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, session, g, flash, request, redirect, url_for,
    current_app
)
from accounts.models import User
from parkings.models import Parking, ParkingSlot, Booking
from common.utils import get_signer
from parkings.forms import ParkingSearchForm
from common.decorators import login_required, is_superuser, is_not_superuser
from datetime import datetime


parkings_app = Blueprint('parkings_app', __name__)


@parkings_app.before_app_request
def load_user():
    g.user = None
    if 'user_id' in session:
        try:
            g.user = User.objects.get(pk=session['user_id'])
        except Exception as e:
            pass


@parkings_app.route('/parkings/search/', methods=['GET', 'POST'])
@is_not_superuser
def search():
    pipeline = [
        {
            '$lookup': {
                'from': 'parkingslot',
                'localField': '_id',
                'foreignField': 'parking_id',
                'as': 'parking_slots'
            }
        }
    ]
    parkings = Parking.objects.aggregate(pipeline)
    return render_template('parking/search.html', parkings=parkings)


@parkings_app.route('/parkings/book/<parking_id>', methods=['GET', 'POST'])
@is_not_superuser
def book(parking_id):
    form = ParkingSearchForm()
    if form.validate_on_submit():
        form.save()
        flash(
            u'Successfully booked',
            'success'
        )
        return redirect(url_for('parkings_app.book', parking_id=parking_id))

    pipeline = [
        {
            '$lookup': {
                'from': 'booking',
                'localField': '_id',
                'foreignField': 'parkingslot_id',
                'as': 'bookings'
            }
        }
    ]
    parking = Parking.objects.get(pk=parking_id)
    available_slots = ParkingSlot.objects.filter(parking_id=parking_id)
    return render_template('parking/book.html', form=form, parking_slots=available_slots, parking=parking)


@parkings_app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    query = {
        'start_time__gte': datetime.now(),
        'is_cancelled': False
    }
    if not g.user.is_superuser:
        query['user_id'] = g.user.pk
    bookings = Booking.objects.filter(**query)
    return render_template('parking/bookings.html', bookings=bookings)


@parkings_app.route('/bookings/cancel/<booking_id>', methods=['GET'])
@login_required
def cancel(booking_id):
    booking = Booking.objects.get(pk=booking_id)
    if g.user.is_superuser or g.user.pk == booking.user_id:
        bookings = Booking.objects(pk=booking_id).update(set__is_cancelled=True)
    return redirect(url_for('parkings_app.bookings'))
