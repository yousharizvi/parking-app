# -*- coding: utf-8 -*-
from functools import wraps
from flask import (request, g, redirect, url_for)


def get_page(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        page = request.args.get('page', 1)
        try:
            kwargs['page'] = int(page)
        except:
            kwargs['page'] = 1
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('accounts_app.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def is_superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or not g.user.is_superuser:
            return redirect(url_for('pages_app.access_denied', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_not_superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or g.user.is_superuser:
            return redirect(url_for('pages_app.access_denied', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
