from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS += [
    'gahd.net'
]

MEDIA_ROOT = str(DATA_DIR.joinpath('media'))
