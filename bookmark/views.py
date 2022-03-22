from django.views.generic import ListView, DetailView

from bookmark.models import Bookmark
from core.entry import Entry
from core.models import Tag

RECENTLY = 5


class BookmarkListView(ListView):
    """Bookmark list"""
    paginate_by = RECENTLY**2

    def get_queryset(self):
        return Entry.get_published_bookmark_list()


class BookmarkDetailView(DetailView):
    """Bookmark detail"""
    model = Bookmark
    slug_url_kwarg = 'bookmark_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookmarkListByTagListView(ListView):
    """
    Bookmark list by tag
    """
    paginate_by = RECENTLY

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return Entry.get_published_bookmark_list().filter(tags=tag.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context
