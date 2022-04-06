from uuid import uuid4

from django.db import models
from django.urls import reverse

from core.models import Post
from core.utils.post import PostType


class Bookmark(Post):
    site_url = models.URLField(unique=True)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True, editable=False)
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.BOOKMARK, max_length=10)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid4())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('bookmark:bookmark-detail',
                       kwargs={'bookmark_slug': self.slug})

    def __str__(self):
        return self.title
