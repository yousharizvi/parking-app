# -*- coding: utf-8 -*-
from wtforms import *
from flask_wtf import FlaskForm
from flask_mail import Message

from application import mail
from accounts.models import User


class LoginForm(FlaskForm):

    user = None

    email = TextField(
        label=u'Email',
        validators=[
            validators.required()
        ]
    )

    password = PasswordField(
        label=u'Password',
        validators=[
            validators.required()
        ]
    )

    next = HiddenField()

    def validate_email(form, field):
        email = field.data
        try:
            form.user = User.objects.get(email=email)
        except:
            raise ValidationError(u'Email not found.')

    def validate_password(form, field):
        password = field.data
        if form.user:
            if not form.user.check_password(password):
                raise ValidationError(u'Incorrect password.')


class SignupForm(FlaskForm):

    name = TextField(
        label=u'Name',
        validators=[
            validators.required(),
            validators.length(max=100)
        ]
    )

    email = TextField(
        label=u'E-mail',
        validators=[
            validators.required(),
            validators.length(max=100),
            validators.Email()
        ]
    )

    password = PasswordField(
        label=u'Password',
        validators=[
            validators.required(),
            validators.length(min=6, max=16)
        ]
    )

    password_confirm = PasswordField(
        label=u'Password Confirm',
        validators=[
            validators.required()
        ]
    )


    next = HiddenField()

    def validate_email(form, field):
        email = field.data
        if User.objects.filter(email=email):
            raise ValidationError(u'E-mail in use.')

    def validate_password_confirm(form, field):
        password = form.password.data
        password_confirm = field.data
        if password != password_confirm:
            raise ValidationError(u'Incorrect password.')

    def save(self):
        email = self.email.data
        name = self.name.data
        password = self.password.data

        user = User(name=name, password=password, email=email)
        user.save()
        return user
