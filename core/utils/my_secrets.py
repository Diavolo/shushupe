import secrets
from uuid import uuid4

from django.core.management.utils import get_random_secret_key


def get_my_random_secret_key(length: int = 50):
    """Generate Django like random secret key.

    Args:
        lenght (int, optional): Length of the random string. Defaults to 50.

    Returns:
       string: Random secret key.
    """
    MY_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(MY_STRING_CHARS) for i in range(length))


class RandomSecretKey:
    """Generate random secret keys."""

    def __init__(self):
        self.id = uuid4()
        self.django_secret_key = get_random_secret_key()
        self.flask_secret_key = secrets.token_hex()
        self.secret_key = get_my_random_secret_key()
