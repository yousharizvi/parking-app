# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, session, g, flash, request, redirect, url_for,
    current_app
)
from accounts.models import User
from accounts.forms import (LoginForm, SignupForm)
from common.utils import get_signer


parkings_app = Blueprint('parkings_app', __name__)


@parkings_app.before_app_request
def load_user():
    g.user = None
    if 'user_id' in session:
        print('TRYING')
        try:
            g.user = User.objects.get(_id=session['user_id'])
            print(g.user)
        except Exception as e:
            print(e)
            pass


@parkings_app.route('/login/', methods=['GET', 'POST'])
def search():
    parkings = Parking.objects.all()
    return render_template('parking/search.html', {
        'parkings': parkings
    })
