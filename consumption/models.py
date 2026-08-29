from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from consumption.constants import (
    ALL_FORMAT_CHOICES,
    FORMAT_VALUES_BY_TYPE,
    PLAYLIST_TYPE,
    SECTION_TO_DETAIL_URL,
    SECTION_TO_LIST_URL,
    requires_url,
    section_for,
)
from core.models import Media, Post
from core.utils.post import PostType


class Consumption(Post):
    class ConsumptionType(models.TextChoices):
        ALBUM = "album", "Album"
        ARTICLE = "article", "Article"
        BOOK = "book", "Book"
        COMIC_MANGA = "comic_manga", "Comic/Manga"
        COURSE = "course", "Course"
        GAME = "game", "Game"
        MOVIE = "movie", "Movie"
        PAPER = "paper", "Paper"
        PLAYLIST = "playlist", "Playlist"
        PODCAST = "podcast", "Podcast"
        SERIES = "series", "Series"
        SINGLE = "single", "Single"
        TRACK = "track", "Track"
        TV_SHOW = "tv_show", "TV Show"
        VIDEO = "video", "Video"

    class ConsumptionStatus(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True, editable=False)
    pub_type = models.CharField(
        choices=PostType.POST_TYPES,
        default=PostType.CONSUMPTION,
        max_length=11,
        editable=False,
    )
    consumption_type = models.CharField(max_length=20, choices=ConsumptionType)
    format = models.CharField(
        max_length=20,
        choices=ALL_FORMAT_CHOICES,
        blank=True,
        help_text="How or where the content is consumed (e.g. vinyl, streaming, cinema).",
    )
    consumption_status = models.CharField(max_length=20, choices=ConsumptionStatus)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(blank=True, null=True)
    url = models.URLField(max_length=255, blank=True)
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="16:9 aspect ratio image e.g. 640x360",
    )
    progress = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. page 13/100, season 2/10, episode 3/10, etc.",
    )

    def clean(self):
        super().clean()

        if self.ended_at and self.started_at and self.ended_at < self.started_at:
            raise ValidationError(
                {"ended_at": "Ended at must be on or after started at."}
            )

        if self.consumption_type == PLAYLIST_TYPE and not self.format:
            raise ValidationError({"format": "Format is required for playlists."})

        if self.format:
            valid_formats = FORMAT_VALUES_BY_TYPE.get(self.consumption_type, set())
            if self.format not in valid_formats:
                raise ValidationError(
                    {
                        "format": (
                            f"Invalid format for consumption type "
                            f"'{self.consumption_type}'."
                        )
                    }
                )
            if requires_url(self.consumption_type, self.format, self.url):
                raise ValidationError(
                    {
                        "url": f"URL is required for {self.consumption_type} {self.format}."
                    }
                )

    def get_section(self):
        return section_for(self.consumption_type, self.format)

    def get_absolute_url(self):
        section = section_for(self.consumption_type, self.format)
        if section is None:
            raise ValueError(
                f"Cannot resolve URL for {self.consumption_type!r} "
                f"with format {self.format!r}."
            )
        return reverse(SECTION_TO_DETAIL_URL[section], kwargs={"slug": self.slug})

    def get_section_url(self):
        section = self.get_section()
        if section is None:
            return None
        return reverse(SECTION_TO_LIST_URL[section])

    def __str__(self):
        return self.title
