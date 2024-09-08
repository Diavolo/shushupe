from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from changelog.models import Changelog
from core.utils.post import PostStatus


class ChangelogListView(ListView):
    """Changelog list"""

    def get_queryset(self):
        return (
            Changelog.objects.select_related("author")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED), Q(pub_date__date__lte=timezone.now())
            )
        )


class ChangelogDetailView(View):
    def get(self, request, *args, **kwargs):
        detail = kwargs["changelog_slug"]
        return redirect(f"/changelog/#{detail}")
