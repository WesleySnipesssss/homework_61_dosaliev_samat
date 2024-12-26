from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article



class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 2

    def dispatch(self, request, *args, **kwargs):
        # print(request.user)
        # print(request.user.is_authenticated)
        # print(request.user.is_anonymous)
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context


class ArticleDetailView(DetailView):
    template_name = 'articles/article_view.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleForm
    # model = Article
    # fields = ['title', 'author', 'content', 'tags']

    # def get_success_url(self):
    #     return reverse('article_detail', kwargs={'pk': self.object.pk})
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('accounts:login')


class ArticleUpdateView(UpdateView):
    template_name = 'articles/article_update.html'
    form_class = ArticleForm
    model = Article


class ArticleDeleteView(DeleteView):
    template_name = 'articles/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:articles')
