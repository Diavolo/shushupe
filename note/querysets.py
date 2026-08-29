from django.db.models import Q

from core.entry import Entry


def visible_note_for_user(user):
    """Published notes visible to the current user.
    """
    qs = Entry.get_published_note_list()
    if user.is_authenticated:
        return qs.filter(Q(is_public=True) | Q(author=user))
    return qs.filter(is_public=True)
