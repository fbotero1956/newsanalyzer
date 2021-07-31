from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article, Comment


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'article_edit.html'
    fields = ('title', 'body', )

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
   
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

class ArticleAddCommentView(CreateView):
    model = Comment
    template_name = 'article_add_comment.html'
    fields = ('comment', )
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        obj = self.get_object()
        form.instance.author = self.request.user
        form.instance.article_id = obj.id
        return super().form_valid(form)
    
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
  
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_create.html'
    fields = ('title', 'body', )
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleAboutView(ListView):
    model = Article
    template_name = "about.html"