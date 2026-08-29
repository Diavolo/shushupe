from django.urls import reverse
from django.views.generic import DetailView, ListView

from consumption.constants import (
    SECTION_LEARNING,
    SECTION_LISTENING,
    SECTION_PLAYING,
    SECTION_READING,
    SECTION_TO_FEED_URL,
    SECTION_TO_LIST_URL,
    SECTION_WATCHING,
)
from consumption.models import Consumption
from consumption.querysets import visible_consumptions_for_section
from core.utils.post import RECENTLY


class ConsumptionListView(ListView):
    section = None
    paginate_by = RECENTLY

    def get_queryset(self):
        return visible_consumptions_for_section(self.section, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = self.section
        context["section_url"] = reverse(SECTION_TO_LIST_URL[self.section])
        context["feed_url"] = reverse(SECTION_TO_FEED_URL[self.section])
        return context


class LearningListView(ConsumptionListView):
    section = SECTION_LEARNING


class ListeningListView(ConsumptionListView):
    section = SECTION_LISTENING


class PlayingListView(ConsumptionListView):
    section = SECTION_PLAYING


class ReadingListView(ConsumptionListView):
    section = SECTION_READING


class WatchingListView(ConsumptionListView):
    section = SECTION_WATCHING


class ConsumptionDetailView(DetailView):
    model = Consumption
    slug_url_kwarg = "slug"
    section = None

    def get_queryset(self):
        return visible_consumptions_for_section(self.section, self.request.user)
