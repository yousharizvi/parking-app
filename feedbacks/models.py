# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from datetime import datetime
from application import db
from common.models import BaseDocument
from mongoengine import CASCADE


class Feedback(BaseDocument):
    user_id = db.ReferenceField('User', reverse_delete_rule=CASCADE)
    message = db.StringField(
        verbose_name=u'Feedback message',
        max_length=400
    )
    rating = db.IntField(
        verbose_name=u'Star Rating',
        requried=True
    )

    meta = {}

    def __unicode__(self):
        return self.message
