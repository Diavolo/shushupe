from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += []

MEDIA_ROOT = str(PROJECT_PACKAGE.joinpath('media'))
