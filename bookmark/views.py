from django.db.models import Q, Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from bookmark.models import Bookmark
from core.entry import Entry
from core.models import Tag
from core.utils.post import PostStatus, RECENTLY

RECENTLY **= 2


def get_popular_tags():
    """Get the RECENTLY popular tags"""
    # Popular list: https://stackoverflow.com/a/11127523
    return Tag.objects.annotate(bookmark_count=Count("bookmark")).order_by(
        "-bookmark_count"
    )[:RECENTLY]


def get_number_of_bookmarks_in_the_current_month():
    now = timezone.now()
    return Bookmark.objects.filter(
        Q(pub_date__year=now.year) & Q(pub_date__month=now.month)
    ).count()


class BookmarkListView(ListView):
    """Bookmark list"""

    paginate_by = RECENTLY

    def get_queryset(self):
        return Entry.get_published_bookmark_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = get_popular_tags()
        current_month_amount = get_number_of_bookmarks_in_the_current_month()
        context["current_month_total_bookmarks"] = current_month_amount
        return context


class BookmarkDetailView(DetailView):
    """Bookmark detail"""

    model = Bookmark
    slug_url_kwarg = "bookmark_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = get_popular_tags()
        current_month_amount = get_number_of_bookmarks_in_the_current_month()
        context["current_month_total_bookmarks"] = current_month_amount
        return context


class BookmarkListByTagListView(ListView):
    """
    Bookmark list by tag
    """

    paginate_by = RECENTLY

    def get(self, *args, **kwargs):
        if not self.kwargs["tag_slug"].islower():
            return redirect(
                "bookmark:bookmark-list-by-tag", self.kwargs["tag_slug"].lower()
            )
        return super().get(*args, **kwargs)

    def get_queryset(self):
        return Entry.get_published_bookmark_list().filter(
            tags__slug=self.kwargs["tag_slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = get_popular_tags()
        context["tag"] = Tag.objects.get(slug=self.kwargs["tag_slug"])
        current_month_amount = get_number_of_bookmarks_in_the_current_month()
        context["current_month_total_bookmarks"] = current_month_amount
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q") or None

        if q is None:
            return redirect("bookmark:bookmark-list")

        bookmark_search_result_list = (
            Bookmark.objects.select_related("author")
            .prefetch_related("tags")
            .filter(
                Q(status=PostStatus.PUBLISHED),
                Q(pub_date__date__lte=timezone.now()),
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(tags__name__icontains=q),
            )
            .order_by("-pub_date")
            .distinct()
        )

        search_result_list = bookmark_search_result_list
        popular_tags = get_popular_tags()
        current_month_amount = get_number_of_bookmarks_in_the_current_month()
        current_month_total_bookmarks = current_month_amount

        return render(
            request,
            "bookmark/search_result.html",
            {
                "search_result_list": search_result_list,
                "search_term": q,
                "current_month_total_bookmarks": current_month_total_bookmarks,
                "popular_tags": popular_tags,
            },
        )
