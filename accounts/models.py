# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from datetime import datetime
from application import db
from common.models import BaseDocument

class User(BaseDocument):
    name = db.StringField(
        verbose_name=u'name',
        max_length=100
    )

    email = db.EmailField(
        verbose_name=u'email',
        max_length=100,
        required=True,
        unique=True
    )

    pw_hash = db.StringField(
        verbose_name=u'senha',
        max_length=100,
        required=True
    )

    is_superuser = db.BooleanField(
        verbose_name=u'super usuário',
        default=False
    )

    meta = {
        'indexes': ['email']
    }

    def __unicode__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super(User, self).__init__(*args, **kwargs)
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(
            password, method=current_app.config['PROJECT_PASSWORD_HASH_METHOD']
        )

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
