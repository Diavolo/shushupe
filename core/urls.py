from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView

from . import views, feeds

app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # REDIRECTS

    path('favicon.ico',
         RedirectView.as_view(url='static/img/favicon.ico', permanent=True),
         name='favicon'),
    path('index.xml', RedirectView.as_view(url='/feed/'), name='go-to-feed'),

    # OTHER SECTIONS WITH CUSTOM URLS

    path('humans.txt',
         TemplateView.as_view(template_name="core/humans.txt",
                              content_type='text/plain'),
         name='humans'),
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('feed/', feeds.LatestEntriesFeed(), name='feed'),
    path('feed/json/', views.JsonFeedView.as_view(), name='json-feed'),
    path('search/', views.SearchView.as_view(), name='search'),

    # TAGS

    path('tags/', views.TagListView.as_view(), name='tag-list'),
    # posts (articles, pages, and notes) by tag
    path('tags/<slug:tag_slug>/', views.PostsByTagListView.as_view(),
         name='post-list-by-tag'),
    # posts by tag feed
    path('tags/<slug:tag_slug>/feed/', feeds.EntriesByTagFeed(),
         name='post-list-by-tag-feed'),

    # PAGES AND ARTICLES

    # page detail or articles by category
    path('<slug:page_slug>/', views.PageOrCategoryView.as_view(),
         name='page-detail-or-article-list-by-category'),
    # articles by category feed
    path('<slug:category_slug>/feed/', feeds.EntriesByCategoryFeed(),
         name='article-list-by-category-feed'),
    # article detail
    path('<slug:category_slug>/<slug:article_slug>/',
         views.ArticleDetailView.as_view(), name='article-detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
