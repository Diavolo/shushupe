from itertools import chain
from operator import attrgetter

from django.db.models import Q
from django.utils import timezone

from bookmark.models import Bookmark
from core.models import Article, Page
from core.utils.post import PostStatus
from note.models import Note


class Entry:
    """Entries"""

    @staticmethod
    def get_post_list(filter_public_post=False):
        """
        Get entries list
        """
        articles = Entry.get_published_article_list()
        notes = Entry.get_published_note_list()
        if filter_public_post:
            articles = articles.filter(is_public=True)
            notes = notes.filter(is_public=True)
        # https://docs.python.org/3/howto/sorting.html#operator-module-functions
        return sorted(chain(articles, notes), key=attrgetter("pub_date"), reverse=True)

    @staticmethod
    def get_published_article_list():
        """
        Get published article list with pub_date less than or equal to today
        """
        return (
            Article.objects.select_related("author")
            .prefetch_related("category")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED), Q(pub_date__date__lte=timezone.now())
            )
        )

    @staticmethod
    def get_published_note_list():
        """
        Get published note list with pub_date less than or equal to today
        """
        return (
            Note.objects.select_related("author")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED), Q(pub_date__date__lte=timezone.now())
            )
        )

    @staticmethod
    def get_published_page_list():
        """
        Get published page list with pub_date less than or equal to today
        """
        return (
            Page.objects.select_related("author")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED), Q(pub_date__date__lte=timezone.now())
            )
        )

    @staticmethod
    def get_published_bookmark_list():
        """
        Get published bookmark list with pub_date less than or equal to today
        """
        return (
            Bookmark.objects.select_related("author")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED), Q(pub_date__date__lte=timezone.now())
            )
        )
