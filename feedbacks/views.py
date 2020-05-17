# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, session, g, flash, request, redirect, url_for,
    current_app
)
from common.utils import get_signer
from accounts.models import User
from feedbacks.models import Feedback
from feedbacks.forms import FeedbackForm
from common.decorators import login_required, is_superuser, is_not_superuser

feedbacks_app = Blueprint('feedbacks_app', __name__)


@feedbacks_app.before_app_request
def load_user():
    g.user = None
    if 'user_id' in session:
        try:
            g.user = User.objects.get(pk=session['user_id'])
        except Exception as e:
            pass


@feedbacks_app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        form.save()
        flash(
            u'Thank you for your feedback',
            'success'
        )
        return redirect(url_for('parkings_app.search'))
    feedbacks = Feedback.objects.filter()
    return render_template('feedbacks/feedbacks.html', form=form, feedbacks=feedbacks)
