from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    path('', views.NoteListView.as_view(), name='note-list'),
    path('<slug:note_slug>/', views.NoteDetailView.as_view(),
         name='note-detail'),
]
