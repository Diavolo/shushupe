from django.urls import path

from review import feeds

from . import views

app_name = "review"
urlpatterns = [
    path("", views.ReviewListView.as_view(), name="review-list"),
    path("feed/", feeds.LatestReviewsFeed(), name="reviews-feed"),
    path(
        "<slug:review_slug>/",
        views.ReviewTopicOrReviewView.as_view(),
        name="review-topic-or-review-detail",
    ),
    path(
        "<slug:review_topic_slug>/<slug:review_slug>/",
        views.ReviewTopicReviewView.as_view(),
        name="review-topic-review-detail",
    ),
    path(
        "<slug:review_topic_slug>/<slug:review_subtopic_slug>/<slug:review_slug>/",
        views.ReviewTopicReviewSubtopicReviewDetailView.as_view(),
        name="review-topic-review-subtopic-review-detail",
    ),
]
