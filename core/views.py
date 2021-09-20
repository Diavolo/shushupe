from datetime import date
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import (Article, Bookmark, Category, Changelog, Note, Page, Post,
                     Tag)

RECENTLY = 5
TODAY = date.today()


class IndexView(ListView):
    template_name = 'core/index.html'
    paginate_by = RECENTLY

    def get_queryset(self):
        print('usuario', self.request.user)
        return PostList.get_post_list(True)[:RECENTLY]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_post_list(True)[:RECENTLY]
        return context


class ArticleListView(ListView):
    """Article list"""
    paginate_by = RECENTLY

    def get_queryset(self):
        return PostList.get_published_article_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_published_article_list()[:RECENTLY]
        context['categories'] = Category.objects.all()
        return context


class ArticlesByCategoryListView(ListView):
    """Article list by category"""
    paginate_by = RECENTLY

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        return PostList.get_published_article_list().filter(category=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(
            slug=self.kwargs['category_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_published_article_list()[:RECENTLY]
        return context


class ArticlesByTagListView(ListView):
    """Article list by tag"""
    paginate_by = RECENTLY

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return PostList.get_published_article_list().filter(tags=tag.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_published_article_list()[:RECENTLY]
        return context


class PostsByTagListView(ListView):
    """Post list by tag"""
    paginate_by = RECENTLY
    template_name = 'core/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = PostList.get_published_article_list().filter(tags=tag.id)
        notes = PostList.get_published_note_list().filter(tags=tag.id)
        pages = PostList.get_published_page_list().filter(tags=tag.id)
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
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=TODAY),
            Q(name__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        article_search_result_list = article_search_result_list.distinct()
        bookmark_search_result_list = Bookmark.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=TODAY),
            Q(name__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        bookmark_search_result_list = bookmark_search_result_list.distinct()
        note_search_result_list = Note.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=TODAY),
            Q(name__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        note_search_result_list = note_search_result_list.distinct()
        page_search_result_list = Page.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(pub_date__date__lte=TODAY),
            Q(name__icontains=q) |
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
        page = Page.objects.filter(slug=self.kwargs['page_slug'])
        if page.count() != 0:
            return render(
                request, 'core/page_detail.html', {'page': page.first()}
            )
        category = Category.objects.get(slug=self.kwargs['page_slug'])
        context = dict()
        context['post_list'] = PostList.get_published_article_list().filter(
            category=category.id
        )
        context['category'] = category
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_published_article_list()[:RECENTLY]
        return render(request, 'core/post_list.html', context)


class ArticleDetailView(DetailView):
    """Article detail"""
    model = Article
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_published_article_list()[:RECENTLY]
        context['categories'] = Category.objects.all()
        context['previous_article'] = PostList.get_published_article_list()\
            .filter(pub_date__lt=self.object.pub_date)\
            .order_by('-pub_date').first()
        context['next_article'] = PostList.get_published_article_list()\
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


class NoteListView(ListView):
    """Note list"""
    model = Note
    paginate_by = RECENTLY

    def get_queryset(self):
        return PostList.get_published_note_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NoteDetailView(DetailView):
    """Note detail"""
    model = Note
    slug_url_kwarg = 'note_slug'


class TagListView(ListView):
    """Tag list"""
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookmarkListView(ListView):
    """Bookmark list"""
    paginate_by = RECENTLY**2

    def get_queryset(self):
        return PostList.get_published_bookmark_list()


class BookmarkDetailView(DetailView):
    """Bookmark detail"""
    model = Bookmark
    slug_url_kwarg = 'bookmark_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookmarkListByTagListView(ListView):
    """
    Bookmark list by tag
    """
    paginate_by = RECENTLY

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return PostList.get_published_bookmark_list().filter(tags=tag.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context


class ChangelogListView(ListView):
    """Changelog list"""

    def get_queryset(self):
        return Changelog.objects.filter(
            Q(status=Post.PUBLISHED_STATUS) |
            Q(pub_date__date__lte=TODAY)
        )


class ChangelogDetailView(View):
    def get(self, request, *args, **kwargs):
        detail = kwargs['changelog_slug']
        return redirect(f'/changelog/#{detail}')


class PostList():
    """Post list"""

    def get_post_list(filter_public_post=False):
        """Post list"""
        articles = PostList.get_published_article_list()
        notes = PostList.get_published_note_list()
        if filter_public_post:
            articles = articles.filter(is_public=True)
            notes = notes.filter(is_public=True)
        # https://docs.python.org/3/howto/sorting.html#operator-module-functions
        return sorted(
            chain(articles, notes), key=attrgetter('pub_date'), reverse=True
        )

    def get_published_article_list():
        """
        Get published article list with pub_date less than or equal to today
        """
        return Article.objects.filter(
            Q(status=Post.PUBLISHED_STATUS) |
            Q(pub_date__date__lte=TODAY)
        )

    def get_published_note_list():
        """
        Get published note list with pub_date less than or equal to today
        """
        return Note.objects.filter(
            Q(status=Post.PUBLISHED_STATUS) |
            Q(pub_date__date__lte=TODAY)
        )

    def get_published_page_list():
        """
        Get published page list with pub_date less than or equal to today
        """
        return Page.objects.filter(
            Q(status=Post.PUBLISHED_STATUS) |
            Q(pub_date__date__lte=TODAY)
        )

    def get_published_bookmark_list():
        """
        Get published bookmark list with pub_date less than or equal to today
        """
        return Bookmark.objects.filter(
            Q(status=Bookmark.PUBLISHED_STATUS) |
            Q(pub_date__date__lte=TODAY)
        )
