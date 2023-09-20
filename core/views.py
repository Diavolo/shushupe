from itertools import chain
from operator import attrgetter
import random

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from bookmark.models import Bookmark
from core.entry import Entry
from core.feeds import latest_entries_json_feed
from core.models import Article, Category, Page, Tag
from core.utils.post import RECENTLY, PostStatus
from note.models import Note


class IndexView(ListView):
    template_name = 'core/index.html'
    paginate_by = RECENTLY
    featured_image = ['escudo', 'inti']

    def get_queryset(self):
        return Entry.get_post_list(True)[:RECENTLY]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = Entry.get_post_list(True)[:RECENTLY]
        context['featured_image'] = self.get_featured_image()
        return context

    def get_featured_image(self):
        return f'img/{random.choice(self.featured_image)}.png'


class JsonFeedView(View):
    def get(self, request, *args, **kwargs):
        json_feed = latest_entries_json_feed()
        return JsonResponse(json_feed)


class ArticleListView(ListView):
    """Article list"""
    paginate_by = RECENTLY

    def get_queryset(self):
        return Entry.get_published_article_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = Entry.get_published_article_list()[
            :RECENTLY]
        context['categories'] = Category.objects.all()
        return context


class ArticlesByCategoryListView(ListView):
    """Article list by category"""
    paginate_by = RECENTLY

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        return Entry.get_published_article_list().filter(category=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(
            slug=self.kwargs['category_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = Entry.get_published_article_list()[
            :RECENTLY]
        return context


class ArticlesByTagListView(ListView):
    """Article list by tag"""
    paginate_by = RECENTLY

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return Entry.get_published_article_list().filter(tags=tag.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = Entry.get_published_article_list()[
            :RECENTLY]
        return context


class PostsByTagListView(ListView):
    """Post (articles, pages, and notes) list by tag"""
    paginate_by = RECENTLY
    template_name = 'core/post_list.html'
    context_object_name = 'post_list'

    def get(self, *args, **kwargs):
        if not self.kwargs['tag_slug'].islower():
            return redirect('core:post-list-by-tag',
                            self.kwargs['tag_slug'].lower())
        return super(PostsByTagListView, self).get(*args, **kwargs)

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = Entry.get_published_article_list().filter(tags=tag.id)
        notes = Entry.get_published_note_list().filter(tags=tag.id)
        pages = Entry.get_published_page_list().filter(tags=tag.id)
        return sorted(
            chain(articles, notes, pages),
            key=attrgetter('pub_date'), reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q') or None
        if q is None:
            return render(request, 'core/search_result.html')
        # https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects
        article_search_result_list = Article.objects.filter(
            Q(status=PostStatus.PUBLISHED),
            Q(pub_date__date__lte=timezone.now()),
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        article_search_result_list = article_search_result_list.distinct()
        bookmark_search_result_list = Bookmark.objects.filter(
            Q(status=PostStatus.PUBLISHED),
            Q(pub_date__date__lte=timezone.now()),
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        bookmark_search_result_list = bookmark_search_result_list.distinct()
        note_search_result_list = Note.objects.filter(
            Q(status=PostStatus.PUBLISHED),
            Q(pub_date__date__lte=timezone.now()),
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        note_search_result_list = note_search_result_list.distinct()
        page_search_result_list = Page.objects.filter(
            Q(status=PostStatus.PUBLISHED),
            Q(pub_date__date__lte=timezone.now()),
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        page_search_result_list = page_search_result_list.distinct()
        search_result_list = sorted(
            chain(article_search_result_list,
                  bookmark_search_result_list,
                  note_search_result_list,
                  page_search_result_list),
            key=attrgetter('pub_date'), reverse=True
        )
        return render(
            request, 'core/search_result.html',
            {'search_result_list': search_result_list, 'search_term': q}
        )


class PageOrCategoryView(View):
    """Page or Articles by Category"""

    def get(self, request, *args, **kwargs):
        if not self.kwargs['page_slug'].islower():
            return redirect('core:page-detail-or-article-list-by-category',
                            self.kwargs['page_slug'].lower())

        page = Page.objects.filter(slug=self.kwargs['page_slug'])
        if page.count() != 0:
            return render(
                request, 'core/page_detail.html', {'page': page.first()}
            )
        category = Category.objects.get(slug=self.kwargs['page_slug'])
        context = dict()
        context['post_list'] = Entry.get_published_article_list()\
                                    .filter(category=category.id)
        context['category'] = category
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = Entry.get_published_article_list()[
            :RECENTLY]
        return render(request, 'core/post_list.html', context)


class ArticleDetailView(DetailView):
    """Article detail"""
    model = Article
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = Entry.get_published_article_list()[
            :RECENTLY]
        context['categories'] = Category.objects.all()
        context['previous_article'] = Entry.get_published_article_list()\
            .filter(pub_date__lt=self.object.pub_date)\
            .order_by('-pub_date').first()
        context['next_article'] = Entry.get_published_article_list()\
            .filter(pub_date__gt=self.object.pub_date)\
            .order_by('pub_date').first()
        return context


class PageDetailView(DetailView):
    """Page detail"""
    model = Page
    slug_url_kwarg = 'page_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagListView(ListView):
    """Tag list"""
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
