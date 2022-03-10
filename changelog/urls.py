from django.urls import path

from . import views

app_name = 'changelog'
urlpatterns = [
    path('', views.ChangelogListView.as_view(),
         name='changelog-list'),
    path('<slug:changelog_slug>/',
         views.ChangelogDetailView.as_view(), name='changelog-detail'),
]
