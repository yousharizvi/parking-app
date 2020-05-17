# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, session, g, flash, request, redirect, url_for,
    current_app
)
from accounts.models import User
from accounts.forms import (LoginForm, SignupForm)
from common.utils import get_signer


accounts_app = Blueprint('accounts_app', __name__)


@accounts_app.before_app_request
def load_user():
    g.user = None
    if 'user_id' in session:
        try:
            g.user = User.objects.get(pk=session['user_id'])
        except:
            pass


@accounts_app.route('/login/', methods=['GET', 'POST'])
def login():
    next = request.values.get('next', '/')
    form = LoginForm()
    form.next.data = next
    if form.validate_on_submit():
        session['user_id'] = str(form.user.pk)
        flash(u'Login successfully', 'success')
        return redirect(next)
    return render_template('accounts/login.html', form=form)


@accounts_app.route('/logout/')
def logout():
    next = request.args.get('next', '/')
    flash(u'Logout successfully', 'success')
    session.pop('user_id', None)
    return redirect(next)


@accounts_app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        form.save()
        flash(
            u'Successfully registered',
            'success'
        )
        return redirect(url_for('accounts_app.login'))
    return render_template('accounts/signup.html', form=form)
