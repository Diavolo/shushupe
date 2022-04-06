from django.db import models
from django.urls import reverse

from core.models import Post
from core.utils.post import PostType


class Note(Post):
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.NOTE, max_length=10)

    def get_absolute_url(self):
        return reverse('note:note-detail', kwargs={'note_slug': self.slug})

    def __str__(self):
        return self.title
