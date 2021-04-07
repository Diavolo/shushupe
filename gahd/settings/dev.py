from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += []

# https://docs.djangoproject.com/en/3.2/ref/settings/#media-root
MEDIA_ROOT = str(PROJECT_PACKAGE.joinpath('media'))
