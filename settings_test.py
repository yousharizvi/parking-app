# -*- coding: utf-8 -*-
from settings import *

# flask core settings
TESTING = True

# flask wtf settings
WTF_CSRF_ENABLED = False

# flask mongoengine settings
MONGODB_SETTINGS = {
    'DB': 'parkingapp_test'
}

# password hash method
PROJECT_PASSWORD_HASH_METHOD = 'md5'
