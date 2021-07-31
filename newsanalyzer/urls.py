from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleUpdateView,
    ArticleCreateView,
    ArticleAboutView,
    ArticleAddCommentView,
) 

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/comment', ArticleAddCommentView.as_view(), name='article_add_comment'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('about/', ArticleAboutView.as_view(), name='about'),
]