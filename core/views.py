from operator import attrgetter
from itertools import chain
from django.views import View
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, render
from django.db.models import Q

from .models import Article, Category, Note, Page, Post, Tag

RECENTLY = 5


class IndexView(ListView):
    template_name = 'core/index.html'
    paginate_by = RECENTLY

    def get_queryset(self):
        print('usuario', self.request.user)
        return PostList.get_post_list()[:RECENTLY]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_post_list()[:RECENTLY]
        return context


class ArticleListView(ListView):
    """Article list"""
    paginate_by = RECENTLY

    def get_queryset(self):
        return PostList.get_article_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_article_list()[:RECENTLY]
        context['categories'] = Category.objects.all()
        return context


class ArticlesByCategoryListView(ListView):
    """Article list by category"""
    paginate_by = RECENTLY

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        return PostList.get_article_list().filter(category=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(
            slug=self.kwargs['category_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_article_list()[:RECENTLY]
        return context


class ArticlesByTagListView(ListView):
    """Article list by tag"""
    paginate_by = RECENTLY

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return PostList.get_article_list().filter(tags=tag.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_article_list()[:RECENTLY]
        return context


class PostsByTagListView(ListView):
    """Post list by tag"""
    paginate_by = RECENTLY
    template_name = 'core/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = PostList.get_article_list().filter(tags=tag.id,
                                                      is_public=True)
        notes = PostList.get_note_list().filter(tags=tag.id, is_public=True)
        pages = PostList.get_page_list().filter(tags=tag.id, is_public=True)
        return sorted(
            chain(articles, notes, pages), key=attrgetter('pub_date'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q') or None
        if q is None:
            return(redirect('/'))
        # https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects
        article_search_result_list = Article.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(name__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        article_search_result_list = article_search_result_list.distinct()
        note_search_result_list = Note.objects.filter(
            Q(status=Post.PUBLISHED_STATUS),
            Q(name__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        )
        note_search_result_list = note_search_result_list.distinct()
        search_result_list = sorted(
            chain(article_search_result_list, note_search_result_list),
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
        context['article_list'] = PostList.get_article_list().filter(
            category=category.id
        )
        context['category'] = category
        context['categories'] = Category.objects.all()
        context['latest_article_list'] = PostList.get_article_list()[:RECENTLY]
        return render(request, 'core/article_list.html', context)


class ArticleDetailView(DetailView):
    """Article detail"""
    model = Article
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article_list'] = PostList.get_article_list()[:RECENTLY]
        context['categories'] = Category.objects.all()
        context['previous_article'] = PostList.get_article_list()\
            .filter(pub_date__lt=self.object.pub_date)\
            .order_by('-pub_date').first()
        context['next_article'] = PostList.get_article_list()\
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


class PostList():
    """Post list"""

    def get_post_list(filter_public_post=False):
        """Post list"""
        articles = PostList.get_article_list()
        notes = PostList.get_note_list()
        if filter_public_post:
            articles = articles.filter(is_public=True)
            notes = notes.filter(is_public=True)
        # https://docs.python.org/3/howto/sorting.html#operator-module-functions
        return sorted(
            chain(articles, notes), key=attrgetter('pub_date'), reverse=True
        )

    def get_article_list():
        """Article list"""
        return Article.objects.filter(
            Q(status=Post.PUBLISHED_STATUS)
        )

    def get_page_list():
        """Page list"""
        return Page.objects.filter(
            Q(status=Post.PUBLISHED_STATUS)
        )

    def get_note_list():
        """Note list"""
        return Note.objects.filter(
            Q(status=Post.PUBLISHED_STATUS)
        )
