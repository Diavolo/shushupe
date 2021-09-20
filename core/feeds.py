from django.conf import settings
from itertools import chain
from operator import attrgetter
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from .views import Category, PostList, Tag, RECENTLY


site_name = settings.SITE_NAME
site_url = settings.SITE_URL
passwd_protected_msg = 'Post protected with a password. ' + \
                       'If you know the password, enter the site and write it.'


class LatestEntriesFeed(Feed):
    title = site_name
    link = '/'
    subtitle = 'Latest posts'
    feed_type = Atom1Feed
    feed_copyright = f'{site_name} - {site_url}'

    def items(self):
        return PostList.get_post_list(True)[:RECENTLY]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return passwd_protected_msg
        return item.content_html[:250] + \
            '...' if item.content_html[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return site_url

    def item_copyright(self):
        return self.feed_copyright


class EntriesByCategoryFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{site_name} - {site_url}'

    def get_object(self, request, category_slug):
        return get_object_or_404(Category, slug=category_slug)

    def title(self, obj):
        return f'{site_name}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest posts in: {obj.name}'

    def link(self, obj):
        return f'/feed/{obj.name}/'

    def items(self, obj):
        return PostList.get_published_article_list()\
                       .filter(category=obj.id, is_public=True)[:RECENTLY]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return passwd_protected_msg
        return item.content_html[:250] + \
            '...' if item.content_html[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return site_name

    def item_copyright(self):
        return self.feed_copyright


class EntriesByTagFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{site_name} - {site_url}'

    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def title(self, obj):
        return f'{site_name}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest posts in: {obj.name}'

    def link(self, obj):
        return f'/tags/{obj.name}'

    def items(self, obj):
        articles = PostList.get_published_article_list()\
                           .filter(tags=obj.id, is_public=True)
        notes = PostList.get_published_note_list()\
                        .filter(tags=obj.id, is_public=True)
        return sorted(
            chain(articles, notes), key=attrgetter('pub_date'), reverse=True
        )

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return passwd_protected_msg
        return item.content_html[:250] + \
            '...' if item.content_html[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return site_url

    def item_copyright(self):
        return self.feed_copyright


class BookmarksByTagFeed(Feed):
    feed_type = Atom1Feed
    feed_copyright = f'{site_name} - {site_url}'

    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def title(self, obj):
        return f'{site_name}: {obj.name}'

    def subtitle(self, obj):
        return f'Latest bookmarks in: {obj.name}'

    def link(self, obj):
        return f'/tags/{obj.name}'

    def items(self, obj):
        bookmarks = PostList.get_published_bookmark_list()\
                            .filter(tags=obj.id, is_public=True)
        return sorted(
            chain(bookmarks), key=attrgetter('pub_date'),
            reverse=True
        )

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return passwd_protected_msg
        return item.content_html[:250] + \
            '...' if item.content_html[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return site_url

    def item_copyright(self):
        return self.feed_copyright
