from django.db.models import Q
from django.utils import timezone

from consumption.constants import (
    LEARNING_TYPES,
    LISTENING_TYPES,
    PLAYING_TYPES,
    PLAYLIST_LISTENING_FORMATS,
    PLAYLIST_TYPE,
    PLAYLIST_WATCHING_FORMATS,
    READING_TYPES,
    SECTION_LEARNING,
    SECTION_LISTENING,
    SECTION_PLAYING,
    SECTION_READING,
    SECTION_WATCHING,
    WATCHING_TYPES,
)
from consumption.models import Consumption
from core.utils.post import PostStatus


def queryset_for_section(section):
    """Return a filter Q for consumptions that belong to a section."""
    if section == SECTION_LEARNING:
        return Q(consumption_type__in=LEARNING_TYPES)
    if section == SECTION_LISTENING:
        return Q(consumption_type__in=LISTENING_TYPES) | Q(
            consumption_type=PLAYLIST_TYPE,
            format__in=PLAYLIST_LISTENING_FORMATS,
        )
    if section == SECTION_PLAYING:
        return Q(consumption_type__in=PLAYING_TYPES)
    if section == SECTION_READING:
        return Q(consumption_type__in=READING_TYPES)
    if section == SECTION_WATCHING:
        return Q(consumption_type__in=WATCHING_TYPES) | Q(
            consumption_type=PLAYLIST_TYPE,
            format__in=PLAYLIST_WATCHING_FORMATS,
        )
    raise ValueError(f"Unknown section: {section!r}")


def published_consumptions_for_section(section):
    """Published consumptions in a section with pub_date on or before today."""
    return (
        Consumption.objects.filter(queryset_for_section(section))
        .filter(
            Q(status=PostStatus.PUBLISHED),
            Q(pub_date__date__lte=timezone.now()),
        )
        .select_related("author", "image")
        .prefetch_related("tags")
        .order_by("-started_at")
    )


def visible_consumptions_for_section(section, user):
    """Published consumptions visible to the current user.

    Public items are always included. The author also sees their own
    private (is_public=False) published items.
    """
    qs = published_consumptions_for_section(section)
    if user.is_authenticated:
        return qs.filter(Q(is_public=True) | Q(author=user))
    return qs.filter(is_public=True)


def public_consumptions_for_section(section):
    """Published, public consumptions in a section (feeds / anonymous)."""
    return published_consumptions_for_section(section).filter(is_public=True)
