from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.utils import timezone

from core.models import Article, Bookmark, Note, Page, Post


class Entry():
    """Entries"""

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
        return sorted(
            chain(articles, notes), key=attrgetter('pub_date'), reverse=True
        )

    def get_published_article_list():
        """
        Get published article list with pub_date less than or equal to today
        """
        return Article.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=timezone.now())
        )

    def get_published_note_list():
        """
        Get published note list with pub_date less than or equal to today
        """
        return Note.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=timezone.now())
        )

    def get_published_page_list():
        """
        Get published page list with pub_date less than or equal to today
        """
        return Page.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=timezone.now())
        )

    def get_published_bookmark_list():
        """
        Get published bookmark list with pub_date less than or equal to today
        """
        return Bookmark.objects.filter(
            Q(status=Bookmark.PUBLISHED_STATUS),
            Q(pub_date__date__lte=timezone.now())
        )
