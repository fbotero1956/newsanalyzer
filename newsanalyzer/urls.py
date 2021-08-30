from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleAboutView,
    ArticleHistoryView,
    FeedHistoryView,
    history_plotter,
    history_plotter_graph,
    rsscall,
) 

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('history/', ArticleHistoryView.as_view(), name='article_history'),
    path('history/plot/', history_plotter, name='history_plotter'),
    path('history_plotter_graph/<str:feed>/', history_plotter_graph,  name='history_plotter_graph'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('about/', ArticleAboutView.as_view(), name='about'),
    path('create/my-ajax-test/', rsscall, name='create/my-ajax-test'),
]