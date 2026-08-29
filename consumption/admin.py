from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from consumption.constants import (
    FORMAT_VALUES_BY_TYPE,
    GROUPED_FORMAT_CHOICES,
    PLAYLIST_TYPE,
)
from consumption.models import Consumption


class ConsumptionForm(forms.ModelForm):
    """Custom validation form for ConsumptionAdmin.

    Args:
        forms (forms.ModelForm): The form to be validated.

    - https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#adding-custom-validation-to-the-admin
    - https://docs.python.org/3/library/functions.html#super
    - https://stackoverflow.com/questions/1060281/in-django-admin-can-i-require-fields-in-a-model-but-not-when-it-is-inline
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["format"].choices = GROUPED_FORMAT_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        consumption_type = cleaned_data.get("consumption_type")
        consumption_format = cleaned_data.get("format")

        if consumption_type == PLAYLIST_TYPE and not consumption_format:
            raise ValidationError({"format": "Format is required for playlists."})

        if consumption_format:
            valid_formats = FORMAT_VALUES_BY_TYPE.get(consumption_type, set())
            if consumption_format not in valid_formats:
                raise ValidationError(
                    {
                        "format": (
                            f"Invalid format for consumption type '{consumption_type}'."
                        )
                    }
                )

        return cleaned_data


class ConsumptionAdmin(admin.ModelAdmin):
    form = ConsumptionForm
    exclude = ("author", "slug")
    search_fields = ("title", "content")
    list_display = (
        "title",
        "creation_date",
        "pub_date",
        "last_modified",
        "status",
        "is_public",
        "protected_with_password",
        "consumption_type",
        "consumption_status",
        "slug",
    )
    list_filter = ("author", "pub_date", "status", "tags")
    filter_horizontal = ("tags",)
    fieldsets = [
        (
            "Consumption info",
            {
                "fields": [
                    "title",
                    "consumption_type",
                    "format",
                    "consumption_status",
                    ("started_at", "ended_at"),
                    "progress",
                    "url",
                    "image",
                    "content",
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
        ("Taxonomy", {"fields": ["tags"], "classes": ["collapse"]}),
    ]
    raw_id_fields = ("image",)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ConsumptionAdmin, self).save_model(request, obj, form, change)

    def post_url(self, obj):
        return obj.slug


admin.site.register(Consumption, ConsumptionAdmin)
