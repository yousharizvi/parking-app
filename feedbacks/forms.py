# -*- coding: utf-8 -*-
from wtforms import *
from flask_wtf import FlaskForm
from flask_mail import Message
from flask_wtf.html5 import NumberInput
from flask import g

from application import mail
from feedbacks.models import Feedback

class FeedbackForm(FlaskForm):
    message = TextField(label=u'Message')
    rating = IntegerField(label=u'Rating', widget=NumberInput(), validators=[validators.NumberRange(min=0, max=5)])

    def save(self):
        user_id = g.user.pk
        rating = self.rating.data
        message = self.message.data
        feedback = Feedback(user_id=user_id, rating=rating, message=message)
        feedback.save()
        return feedback
