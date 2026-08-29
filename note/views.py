from django.views.generic import DetailView, ListView

from core.utils.post import RECENTLY
from note.models import Note
from note.querysets import visible_note_for_user


class NoteListView(ListView):
    """Note list"""

    model = Note
    paginate_by = RECENTLY

    def get_queryset(self):
        return visible_note_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NoteDetailView(DetailView):
    """Note detail"""

    model = Note
    slug_url_kwarg = "note_slug"

    def get_queryset(self):
        return visible_note_for_user(self.request.user)
