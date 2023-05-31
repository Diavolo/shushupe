from mimetypes import guess_type
from os import path
from time import strftime
from uuid import uuid4

import mistune

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import slugify

from core.utils.markdown import HighlightRenderer
from core.utils.post import PostStatus, PostType


renderer = HighlightRenderer()
markdown = mistune.create_markdown(renderer=renderer)


class Taxonomy(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()

    class Meta:
        abstract = True


class Category(Taxonomy):
    class Meta():
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(Taxonomy):
    def __str__(self):
        return self.name


class Post(models.Model):
    """The Post type serves as the base type for most of the other kinds of
    objects such as Article, Page, etc.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT)
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    content_html = models.TextField(editable=False)
    pub_type = models.CharField(choices=PostType.POST_TYPES, max_length=10)
    is_public = models.BooleanField(default=True)
    status = models.CharField(choices=PostStatus.POST_STATUSES,
                              default=PostStatus.PUBLISHED,
                              max_length=9)
    tags = models.ManyToManyField(Tag, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=False)
    protected_with_password = models.BooleanField()
    post_password = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content)
        # TODO: use bcrypt to encrypt post passwd
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        # https://docs.djangoproject.com/en/3.0/ref/models/options/#ordering
        ordering = ('-pub_date',)


class Article(Post):
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.ARTICLE, max_length=10)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('core:article-detail',
                       kwargs={'category_slug': self.category.slug,
                               'article_slug': self.slug})

    def __str__(self):
        return self.title


class Page(Post):
    pub_type = models.CharField(choices=PostType.POST_TYPES,
                                default=PostType.PAGE, max_length=10)
    parent = models.ForeignKey('Page', on_delete=models.SET_NULL,
                               limit_choices_to={'parent': None},
                               blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    author_email = models.EmailField(max_length=100)
    author_url = models.URLField(max_length=200, blank=True)
    author_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    published = models.DateTimeField(auto_now_add=timezone.now)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    karma = models.IntegerField(blank=True)
    approved = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True,
                             default=None)

    class Meta:
        abstract = True
        ordering = ('-published',)


class ArticleComment(Comment):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.title} - {self.author}'


class PageComment(Comment):
    post = models.ForeignKey(Page, on_delete=models.CASCADE)
    parent = models.ForeignKey('PageComment', on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.title} - {self.author}'


def user_directory_path(instance, filename):
    """File will be uploaded to
    MEDIA_ROOT/<YYYY>/<mm>/<file_name>-<uuid1()>-<filex_extension>
    https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField.upload_to
    """
    file_name, file_extension = path.splitext(filename)
    return f'{strftime("%Y")}/{strftime("%m")}/\
        {slugify(file_name)}-{str(uuid4())}{file_extension}'


class Media(models.Model):
    name = models.CharField(max_length=200)
    media_file = models.FileField(upload_to=user_directory_path)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.media_file.name

    def image_thumb(self):
        if self.media_file:
            if guess_type(str(self.media_file))[0].split('/')[0] == 'image':
                return format_html(
                    f'<img src="{settings.MEDIA_URL}{self.media_file}" \
                    width="100px" alt="{self.name}" />')
            else:
                return self.name
        else:
            return 'No file'
