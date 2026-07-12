# django.template.Library.filter()
from urllib.parse import urlparse
from django import template

register = template.Library()


def url_domain(value):
    """URL custom template to show the network location of the saved URI.

    - https://docs.djangoproject.com/en/5.2/howto/custom-template-tags/
    - https://docs.python.org/3/library/urllib.parse.html

    Args:
        value (str): URL's URI

    Returns:
        str: Network Location.
    """
    bookmark = urlparse(value)
    return f"{bookmark.netloc}"


register.filter("url_domain", url_domain)
