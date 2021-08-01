from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Article 


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
   
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
  
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_select.html'
    fields = ('title', 'body', )
    success_url = reverse_lazy('article_list')

#   def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)

class ArticleAboutView(ListView):
    model = Article
    template_name = "about.html"