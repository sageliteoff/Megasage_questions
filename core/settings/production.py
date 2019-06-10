import os
from .base import *


DEBUG = True

ALLOWED_HOSTS = ["192.168.200.5","mainserve"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "megasage",
	"PASSWORD": "megasage",
	"HOST": "localhost",
	"PORT": ""

    }}

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

X_FRAME_OPTIONS = "DENY"
