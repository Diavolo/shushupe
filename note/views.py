from django.views.generic import DetailView, ListView

from core.entry import Entry
from core.utils.post import RECENTLY
from note.models import Note


class NoteListView(ListView):
    """Note list"""

    model = Note
    paginate_by = RECENTLY

    def get_queryset(self):
        return Entry.get_published_note_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NoteDetailView(DetailView):
    """Note detail"""

    model = Note
    slug_url_kwarg = "note_slug"
