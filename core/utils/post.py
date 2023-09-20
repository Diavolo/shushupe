from bs4 import BeautifulSoup
from django.conf import settings

RECENTLY = 5
_site_url = settings.SITE_URL


class PostType:
    ARTICLE = 'Article'
    NOTE = 'Note'
    PAGE = 'Page'
    BOOKMARK = 'Bookmark'
    CHANGELOG = 'Changelog'

    POST_TYPES = sorted(((ARTICLE.lower(), ARTICLE.title()),
                         (NOTE.lower(), NOTE.title()),
                         (PAGE.lower(), PAGE.title())))


class PostStatus:
    PUBLISHED = 'published'
    DRAFT = 'draft'

    POST_STATUSES = sorted(((PUBLISHED.lower(), PUBLISHED.title()),
                            (DRAFT.lower(), DRAFT.title())))


def get_full_path(item_url: str) -> str:
    """Get the complete path of an 'item'.

    Args:
        item_url (str): Item URL (i.e. /about/) without the base name.

    Returns:
        str: Full path of the item (including the base URL i.e. https://...)
    """
    return f"{_site_url}{item_url}"
