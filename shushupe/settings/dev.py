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

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'review': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
