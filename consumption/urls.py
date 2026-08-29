from django.urls import path

from consumption import feeds, views
from consumption.constants import (
    SECTION_LEARNING,
    SECTION_LISTENING,
    SECTION_PLAYING,
    SECTION_READING,
    SECTION_WATCHING,
)


app_name = "consumption"
urlpatterns = [
    path("learning/", views.LearningListView.as_view(), name="learning-list"),
    path("learning/feed/", feeds.LearningFeed(), name="learning-feed"),
    path(
        "learning/<slug:slug>/",
        views.ConsumptionDetailView.as_view(section=SECTION_LEARNING),
        name="learning-detail",
    ),
    path("listening/", views.ListeningListView.as_view(), name="listening-list"),
    path("listening/feed/", feeds.ListeningFeed(), name="listening-feed"),
    path(
        "listening/<slug:slug>/",
        views.ConsumptionDetailView.as_view(section=SECTION_LISTENING),
        name="listening-detail",
    ),
    path("playing/", views.PlayingListView.as_view(), name="playing-list"),
    path("playing/feed/", feeds.PlayingFeed(), name="playing-feed"),
    path(
        "playing/<slug:slug>/",
        views.ConsumptionDetailView.as_view(section=SECTION_PLAYING),
        name="playing-detail",
    ),
    path("reading/", views.ReadingListView.as_view(), name="reading-list"),
    path("reading/feed/", feeds.ReadingFeed(), name="reading-feed"),
    path(
        "reading/<slug:slug>/",
        views.ConsumptionDetailView.as_view(section=SECTION_READING),
        name="reading-detail",
    ),
    path("watching/", views.WatchingListView.as_view(), name="watching-list"),
    path("watching/feed/", feeds.WatchingFeed(), name="watching-feed"),
    path(
        "watching/<slug:slug>/",
        views.ConsumptionDetailView.as_view(section=SECTION_WATCHING),
        name="watching-detail",
    ),
]
