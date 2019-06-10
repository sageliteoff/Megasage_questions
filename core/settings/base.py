import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = 'jk#gjh1z6b141_3bj(x3ub(k4o-wsxcb!oq_4z7*2ga!(ksh&_'

SITE_ID =1

INSTALLED_APPS = [
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    "core",
    'home.apps.HomeConfig',
    "userprofile.apps.UserprofileConfig",
    "subscriptionpackages.apps.SubscriptionpackagesConfig",
    "tinymce",
    "allauth",
    "allauth.account",
    "allauth.socialaccount"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"allauth","templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "core.context_processors.programmes",
            ],
        },
    },]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'


AUTHENCATION_BACKENDS =(
    "django.contrib.auth.ModelBackend",
    "alluath.account.auth_backends.AuthencationBackend")

#allauth settings
ACCOUNT_FORMS ={
    "login": "core.forms.CustomLoginForm",
    "signup": "core.forms.CustomSignupForm"
}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = " none" #mandory none optional
LOGIN_REDIRECT_URL = "/userprofile"
ACCOUNT_USERNAME_MIN_LENGTH = 3

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },]



# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,"static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"allauth/static")
    ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'FILES/')
MEDIA_URL = "/files/"


# FILEBROWSER SETTINGS
FILEBROWSER_DIRECTORY = ""
DIRECTORY = "/"


# TINYMCE SETTINGS
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    "branding": False,
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    "theme": "modern",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    "width": "80%",
    "height": "250px",
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
}
