from .common import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root
MEDIA_ROOT = str(DATA_DIR.joinpath('media'))
