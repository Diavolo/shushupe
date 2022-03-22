from django.urls import path

from . import views
from bookmark import feeds

app_name = 'bookmark'
urlpatterns = [
    path('', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('tags/<slug:tag_slug>/',
         views.BookmarkListByTagListView.as_view(),
         name='bookmark-list-by-tag'),
    path('tags/<slug:tag_slug>/feed/', feeds.BookmarksByTagFeed(),
         name='bookmark-list-by-tag-feed'),
    path('<slug:bookmark_slug>/', views.BookmarkDetailView.as_view(),
         name='bookmark-detail'),
]
