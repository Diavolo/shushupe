from .common import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# debug_toolbar config
DEV_APPS = [
    "debug_toolbar",
]

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS

DEV_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]
