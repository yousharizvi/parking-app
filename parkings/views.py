# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, session, g, flash, request, redirect, url_for,
    current_app
)
from accounts.models import User
from parkings.models import Parking, ParkingSlot
from common.utils import get_signer
from parkings.forms import ParkingSearchForm
from common.decorators import login_required, is_superuser, is_not_superuser

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
