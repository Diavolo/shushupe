# django.template.Library.filter()
from urllib.parse import urlparse
from django import template

register = template.Library()


def bookmark_domain(value):
    """Bookmark custom template to show the network location of the saved URI.

    - https://docs.djangoproject.com/en/5.2/howto/custom-template-tags/
    - https://docs.python.org/3/library/urllib.parse.html

    Args:
        value (str): Bookmark's URI

    Returns:
        str: Network Location.
    """
    bookmark = urlparse(value)
    return f"{bookmark.netloc}"


register.filter("bookmark_domain", bookmark_domain)
