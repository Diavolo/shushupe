from uuid import uuid4

from django.db import models

from core.models import Post
from core.utils.post import PostType


class Changelog(Post):
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.CHANGELOG, max_length=10)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
