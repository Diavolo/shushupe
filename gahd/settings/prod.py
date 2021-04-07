import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS += [
    'gahd.net'
]

# https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = 3600

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-referrer-policy
SECURE_REFERRER_POLICY = 'same-origin'

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True

# https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#media-root
MEDIA_ROOT = str(DATA_DIR.joinpath('media'))

# https://docs.sentry.io/platforms/python/guides/django/#configure
sentry_sdk.init(
    dsn=str(SECRETS['sentry']),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
