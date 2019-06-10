import os
from .base import *


DEBUG = True



ALLOWED_HOSTS = ["localhost","192.168.43.5", "192.168.200.10", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }}
