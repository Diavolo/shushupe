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


def get_post_reference(post_url: str) -> str:
    return f"{_site_url}{post_url}"
