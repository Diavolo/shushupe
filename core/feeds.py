from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from .views import Category, PostList, Tag


site_name = settings.SITE_NAME
site_url = settings.SITE_URL


class LatestEntriesFeed(Feed):
    title = site_name
    link = '/'
    subtitle = 'Últimos artículos publicados'
    feed_type = Atom1Feed
    feed_copyright = f'{site_name} - {site_url}'

    def items(self):
        return PostList.get_article_list().filter(is_public=True)[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return 'Entrada protegida. ' + \
                   'Si conoce la clave de acceso, ' + \
                   'ingrese al sitio para ingresar la contraseña.'
        return item.content_html[:250] + \
            '...' if item.content[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.updated_date

    def item_author_name(self, item):
        return item.author

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
        return f'Últimas entradas publicadas en la categoría: {obj.name}'

    def link(self, obj):
        return f'/feed/{obj.name}/'

    def items(self, obj):
        return PostList.get_article_list().filter(category=obj.id,
                                                  is_public=True)[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return 'Entrada protegida. ' + \
                   'Si conoce la clave de acceso, ' + \
                   'ingrese al sitio para ingresar la contraseña.'
        return item.content_html[:250] + \
            '...' if item.content[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.updated_date

    def item_author_name(self, item):
        return item.author

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
        return f'Últimas entradas publicadas con el tag: {obj.name}'

    def link(self, obj):
        return f'/tags/{obj.name}'

    def items(self, obj):
        return PostList.get_article_list().filter(tags=obj.id,
                                                  is_public=True)[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        if item.protected_with_password:
            return 'Entrada protegida. ' + \
                   'Si conoce la clave de acceso, ' + \
                   'ingrese al sitio para ingresar la contraseña.'
        return item.content_html[:250] + \
            '...' if item.content[250:] else item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.updated_date

    def item_author_name(self, item):
        return item.author

    def item_author_link(self):
        return site_url

    def item_copyright(self):
        return self.feed_copyright
