from itertools import chain
from operator import attrgetter

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from core.entry import Entry
from core.models import Tag
from core.utils.constants import PASSWD_PROTECTED_MSG
from core.utils.post import get_full_path
from core.utils.shushupe import SITE_NAME, SITE_URL


class BookmarksByTagFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{SITE_NAME} - {SITE_URL}'

    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def title(self, obj):
        return f'{SITE_NAME}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest bookmarks in: {obj.name}'

    def link(self, obj):
        return f'/tags/{obj.name}'

    def items(self, obj):
        bookmarks = Entry.get_published_bookmark_list()\
                         .filter(tags=obj.id, is_public=True)
        return sorted(
            chain(bookmarks), key=attrgetter('pub_date'),
            reverse=True
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.protected_with_password:
            return PASSWD_PROTECTED_MSG
        return item.content_html + get_full_path(item.get_absolute_url())

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return SITE_URL

    def item_copyright(self):
        return self.feed_copyright
