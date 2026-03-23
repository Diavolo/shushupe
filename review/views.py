import logging

from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from core.utils.post import RECENTLY
from review.models import Review, ReviewTopic

logger = logging.getLogger(__name__)


# /reviews/
class ReviewListView(ListView):
    slug_url_kwarg = "review_slug"
    template_name = "review/review_list.html"
    context_object_name = "review_list"
    paginate_by = RECENTLY

    def get_queryset(self, *args, **kwargs):
        return Review.objects.select_related(
            "review_topic", "review_topic__parent", "item_image", "review_topic__image"
        ).prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the 4 latest topics that have reviews
        latest_review_topics = (
            ReviewTopic.objects.filter(review__isnull=False)
            .select_related("image", "parent")
            .annotate(latest_review_date=models.Max("review__pub_date"))
            .order_by("-latest_review_date")[:4]
        )

        context["latest_review_topics"] = latest_review_topics
        return context


# /reviews/<slug:review_slug>/
class ReviewTopicOrReviewView(View):
    def get(self, request, *args, **kwargs):
        review_topic = (
            ReviewTopic.objects.select_related("parent")
            .filter(slug=kwargs["review_slug"])
            .first()
        )

        # If review topic is not found, then the content is a review, so get view or return 404
        if not review_topic:
            logger.debug("review_topic not found")
            review = get_object_or_404(
                Review.objects.select_related(
                    "review_topic",
                    "review_topic__parent",
                    "item_image",
                    "review_topic__image",
                ).prefetch_related("tags"),
                slug=kwargs["review_slug"],
            )

            # If review has a review topic, then redirect to the review topic view
            if review.review_topic:
                return redirect(
                    "review:review-topic-review-detail",
                    review_topic_slug=review.review_topic.slug,
                    review_slug=kwargs["review_slug"],
                )

            return render(request, "review/review_detail.html", {"review": review})

        # Check if review_topic has a parent, if so, then redirect to the parent/child view
        if review_topic.parent:
            return redirect(
                "review:review-topic-review-subtopic-review-detail",
                review_topic_slug=review_topic.parent.slug,
                review_subtopic_slug=review_topic.slug,
                review_slug=kwargs["review_slug"],
            )

        review = (
            Review.objects.select_related(
                "review_topic",
                "review_topic__parent",
                "item_image",
                "review_topic__image",
            )
            .prefetch_related("tags")
            .filter(slug=kwargs["review_slug"])
            .first()
        )

        review_list = (
            Review.objects.filter(review_topic=review_topic)
            .select_related(
                "review_topic",
                "review_topic__parent",
                "item_image",
                "review_topic__image",
            )
            .prefetch_related("tags")
        )

        context = {
            "review_topic": review_topic,
            "review_list": review_list,
            "review": review,
        }

        return render(request, "review/review_info_list.html", context)


# /reviews/<slug:review_topic_slug>/<slug:review_slug>/
class ReviewTopicReviewView(View):
    def get(self, request, *args, **kwargs):

        review_topic = get_object_or_404(
            ReviewTopic.objects.select_related("parent"),
            slug=kwargs["review_topic_slug"],
        )

        # Check if review_slug is a subtopic
        review_subtopic = ReviewTopic.objects.filter(slug=kwargs["review_slug"]).first()

        if review_topic.parent and not review_subtopic:
            # redirect to review-topic-review-subtopic-review-detail
            return redirect(
                "review:review-topic-review-subtopic-review-detail",
                review_topic_slug=review_topic.parent.slug,
                review_subtopic_slug=review_topic.slug,
                review_slug=kwargs["review_slug"],
            )

        if review_subtopic:
            review_list = (
                Review.objects.filter(review_topic=review_subtopic)
                .select_related(
                    "review_topic",
                    "review_topic__parent",
                    "item_image",
                    "review_topic__image",
                )
                .prefetch_related("tags")
            )

            context = {
                "review_topic": review_subtopic,
                "review_list": review_list,
            }
            return render(request, "review/review_info_list.html", context)

        review = get_object_or_404(
            Review.objects.select_related(
                "review_topic",
                "review_topic__parent",
                "item_image",
                "review_topic__image",
            ).prefetch_related("tags"),
            slug=kwargs["review_slug"],
            review_topic__slug=kwargs["review_topic_slug"],
        )

        context = {"review_topic": review_topic, "review": review}
        return render(request, "review/review_info_list.html", context)


# /reviews/<slug:review_topic_slug>/<slug:review_subtopic_slug>/<slug:review_slug>/
class ReviewTopicReviewSubtopicReviewDetailView(DetailView):
    model = Review
    slug_url_kwarg = "review_slug"
    context_object_name = "review"

    def get_queryset(self):
        return Review.objects.select_related(
            "review_topic", "review_topic__parent", "item_image", "review_topic__image"
        ).prefetch_related("tags")

    def get_object(self):
        # Check if review topic is a parent, if so, return 404
        get_object_or_404(
            ReviewTopic.objects.select_related("parent"),
            slug=self.kwargs["review_topic_slug"],
            parent__isnull=True,
        )

        review = get_object_or_404(
            self.get_queryset(),
            slug=self.kwargs["review_slug"],
            review_topic__slug=self.kwargs["review_subtopic_slug"],
            review_topic__parent__slug=self.kwargs["review_topic_slug"],
        )
        return review
