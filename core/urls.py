from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView

from . import views, feeds

app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favicon.ico', RedirectView.as_view(url='static/img/favicon.ico',
                                             permanent=True),
         name='favicon'),
    path('humans.txt', TemplateView.as_view(template_name="core/humans.txt",
                                            content_type='text/plain'),
         name='humans'),
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('index.xml', RedirectView.as_view(url='/feed/'), name='go-to-feed'),
    path('feed/', feeds.LatestEntriesFeed(), name='feed'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    # articles by tag
    path('tags/<slug:tag_slug>/', views.PostsByTagListView.as_view(),
         name='article-list-by-tag'),
    # articles by tag feed
    path('tags/<slug:tag_slug>/feed/', feeds.EntriesByTagFeed(),
         name='article-list-by-tag-feed'),
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/<slug:note_slug>/', views.NoteDetailView.as_view(),
         name='note-detail'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/tags/<slug:tag_slug>/',
         views.BookmarkListByTagListView.as_view(),
         name='bookmark-list-by-tag'),
    path('bookmarks/tags/<slug:tag_slug>/feed/', feeds.BookmarksByTagFeed(),
         name='bookmark-list-by-tag-feed'),
    path('bookmarks/<slug:bookmark_slug>/', views.BookmarkDetailView.as_view(),
         name='bookmark-detail'),
    path('changelog/', views.ChangelogListView.as_view(),
         name='changelog-list'),
    path('changelog/<slug:changelog_slug>/',
         views.ChangelogDetailView.as_view(), name='changelog-detail'),
    # page detail or articles by category
    path('<slug:page_slug>/', views.PageOrCategoryView.as_view(),
         name='page-detail'),
    path('<slug:page_slug>/', views.PageOrCategoryView.as_view(),
         name='article-list-by-category'),
    # articles by category feed
    path('<slug:category_slug>/feed/', feeds.EntriesByCategoryFeed(),
         name='article-list-by-category-feed'),
    # article detail
    path('<slug:category_slug>/<slug:article_slug>/',
         views.ArticleDetailView.as_view(), name='article-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
