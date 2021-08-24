from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleAboutView,
    ArticleHistoryView,
    rsscall,
) 

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('history/', ArticleHistoryView.as_view(), name='article_history'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('about/', ArticleAboutView.as_view(), name='about'),
    path('create/my-ajax-test/', rsscall, name='create/my-ajax-test'),
]