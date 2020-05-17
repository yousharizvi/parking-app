# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, redirect, g, url_for)


pages_app = Blueprint('pages_app', __name__)


@pages_app.route('/')
def index():
    if not g.user:
        return redirect(url_for('accounts_app.login'))
    elif g.user and g.user.is_superuser:
        return redirect(url_for('parkings_app.bookings'))
    return redirect(url_for('parkings_app.search'))


@pages_app.route('/access_denied/')
def access_denied():
    return render_template('pages/access_denied.html')
