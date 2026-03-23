from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import Media, Post
from core.utils.post import PostType
from review.utils.choices import CurrencyType, RatingType, ReviewTopicType, ReviewType


class ReviewTopic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200)
    review_topic_type = models.CharField(
        choices=ReviewTopicType.REVIEW_TOPIC_TYPES, max_length=10
    )
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="1:1 aspect ratio image e.g. 320x320",
    )
    parent = models.ForeignKey(
        "ReviewTopic",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Parent topic for subtopics (e.g. a saga or franchise)",
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_review_topic_type_display()})"

    def get_absolute_url(self):
        if self.parent:
            return reverse(
                "review:review-topic-review-detail",
                kwargs={
                    "review_topic_slug": self.parent.slug,
                    "review_slug": self.slug,
                },
            )
        return reverse(
            "review:review-topic-or-review-detail", kwargs={"review_slug": self.slug}
        )


class Review(Post):
    pub_type = models.CharField(default=PostType.REVIEW, max_length=10, editable=False)

    review_topic = models.ForeignKey(
        ReviewTopic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    review_type = models.CharField(choices=ReviewType.REVIEW_TYPES, max_length=12)
    rating = models.DecimalField(
        choices=RatingType.RATING_TYPES, max_digits=3, decimal_places=1
    )
    volume = models.IntegerField(
        blank=True, null=True, help_text="Season, volume, or installment number"
    )
    item_number = models.IntegerField(
        blank=True, null=True, help_text="Episode, track, issue, or chapter number"
    )
    item_release_date = models.DateField(blank=True, null=True)
    item_url = models.URLField(max_length=255, blank=True, null=True)
    item_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="1:1 aspect ratio image e.g. 320x320",
    )
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    is_recommended = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(
        choices=CurrencyType.CURRENCY_TYPES,
        max_length=3,
        blank=True,
        help_text="Currency for the listed price",
    )
    location = models.CharField(max_length=255, blank=True)

    def clean(self):
        super().clean()

        has_price = self.price is not None
        has_currency = bool(self.currency)

        if has_price and not has_currency:
            raise ValidationError(
                {"currency": "Currency is required if price is provided"}
            )

        if has_currency and not has_price:
            raise ValidationError(
                {"price": "Price is required if currency is provided"}
            )

    def get_absolute_url(self):
        if self.review_topic:
            if self.review_topic.parent:
                return reverse(
                    "review:review-topic-review-subtopic-review-detail",
                    kwargs={
                        "review_topic_slug": self.review_topic.parent.slug,
                        "review_subtopic_slug": self.review_topic.slug,
                        "review_slug": self.slug,
                    },
                )
            else:
                return reverse(
                    "review:review-topic-review-detail",
                    kwargs={
                        "review_topic_slug": self.review_topic.slug,
                        "review_slug": self.slug,
                    },
                )
        else:
            return reverse(
                "review:review-topic-or-review-detail",
                kwargs={"review_slug": self.slug},
            )

    def __str__(self):
        return self.title

    def get_topic_display(self):
        """Get the display name of the review topic.

        Returns:
            str: The display name of the review topic.
        """
        if self.review_topic:
            return f"{self.review_topic.name} ({self.title})"
        return self.title
