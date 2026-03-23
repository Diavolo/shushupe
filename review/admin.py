from django import forms
from django.contrib import admin

from review.models import Review, ReviewTopic


class ReviewTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_display = ("name", "review_topic_type", "parent", "slug")
    list_filter = ("review_topic_type", "parent")
    raw_id_fields = ("image",)


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    exclude = (
        "author",
    )  # pub_type is already editable=False and default=PostType.REVIEW
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_display = (
        "title",
        "review_type",
        "rating",
        "pub_date",
        "last_modified",
        "status",
        "is_public",
        "protected_with_password",
        "slug",
    )
    list_filter = ("review_type", "review_topic")
    filter_horizontal = ("tags",)
    fieldsets = [
        (
            "Review info",
            {
                "fields": [
                    "title",
                    "slug",
                    "content",
                    "review_type",
                    "rating",
                    "volume",
                    "item_number",
                    "item_release_date",
                    "item_url",
                    "item_image",
                    "pros",
                    "cons",
                    "is_recommended",
                    "price",
                    "currency",
                    "location",
                ]
            },
        ),
        ("Visibility", {"fields": ["is_public", "status"], "classes": ["collapse"]}),
        (
            "Meta",
            {
                "fields": [
                    "pub_date",
                    "allow_comments",
                    "protected_with_password",
                    "post_password",
                ],
                "classes": ["collapse"],
            },
        ),
        ("Taxonomy", {"fields": ["review_topic", "tags"], "classes": ["collapse"]}),
    ]
    raw_id_fields = ("item_image",)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewTopic, ReviewTopicAdmin)
