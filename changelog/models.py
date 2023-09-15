from django.db import models

from core.models import Post
from core.utils.post import PostType


class Changelog(Post):
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.CHANGELOG, max_length=10)

    def __str__(self):
        return self.title
