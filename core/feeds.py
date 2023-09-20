from itertools import chain
from operator import attrgetter

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
import html2text

from core.entry import Entry
from core.models import Category, Tag
from core.utils.constants import PASSWD_PROTECTED_MSG
from core.utils.post import RECENTLY, get_full_path
from core.utils.shushupe import SITE_NAME, SITE_URL


class LatestEntriesFeed(Feed):
    title = SITE_NAME
    link = '/'
    subtitle = 'Latest posts'
    feed_type = Atom1Feed
    feed_copyright = f'{SITE_NAME} - {SITE_URL}'

    def items(self):
        return Entry.get_post_list(True)[:RECENTLY]

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


class EntriesByCategoryFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{SITE_NAME} - {SITE_URL}'

    def get_object(self, request, category_slug):
        return get_object_or_404(Category, slug=category_slug)

    def title(self, obj):
        return f'{SITE_NAME}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest posts in: {obj.name}'

    def link(self, obj):
        return f'/feed/{obj.name}/'

    def items(self, obj):
        return Entry.get_published_article_list()\
                    .filter(category=obj.id, is_public=True)[:RECENTLY]

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
        return SITE_NAME

    def item_copyright(self):
        return self.feed_copyright


class EntriesByTagFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{SITE_NAME} - {SITE_URL}'

    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def title(self, obj):
        return f'{SITE_NAME}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest posts in: {obj.name}'

    def link(self, obj):
        return f'/tags/{obj.name}'

    def items(self, obj):
        articles = Entry.get_published_article_list()\
                        .filter(tags=obj.id, is_public=True)
        notes = Entry.get_published_note_list()\
                     .filter(tags=obj.id, is_public=True)
        return sorted(
            chain(articles, notes), key=attrgetter('pub_date'), reverse=True
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


def latest_entries_json_feed():
    latest_posts = Entry.get_post_list(True)[:RECENTLY]
    return {
        "version": "https://jsonfeed.org/version/1.1",
        "title": SITE_NAME,
        "home_page_url": SITE_URL,
        "feed_url": get_full_path(reverse('core:json-feed')),
        "favicon": get_full_path("/static/img/favicon.png"),
        "items": [
            {
                "id": get_full_path(i.get_absolute_url()),
                "url": get_full_path(i.get_absolute_url()),
                "title": i.title,
                "content_html": i.content_html
                if not i.protected_with_password else PASSWD_PROTECTED_MSG,
                "content_text": html2text.html2text(i.content_html).strip()
                if not i.protected_with_password else PASSWD_PROTECTED_MSG,
                "date_published": i.pub_date,
                "date_modified": i.last_modified,
                "authors": [
                    {
                        "name": f"{i.author.first_name} {i.author.last_name}",
                        "url": SITE_URL,
                        "avatar": get_full_path("/static/img/avatar.png")
                    }
                ],
                "tags": [j.get("slug") for j in (i.tags.values())
                         if len((i.tags.values())) > 0]
            } for i in latest_posts]
    }
