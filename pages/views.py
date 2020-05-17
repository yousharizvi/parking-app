# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


pages_app = Blueprint('pages_app', __name__)


@pages_app.route('/')
def index():
    return render_template('pages/index.html')


@pages_app.route('/access_denied/')
def access_denied():
    return render_template('pages/access_denied.html')
