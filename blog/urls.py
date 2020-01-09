from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchResultsView,
    PostMonthArchiveView,
    TagView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('<int:year>/<str:month>/',
         PostMonthArchiveView.as_view(),
         name="archive-month"),
    path('tag/<str:tagname>', TagView.as_view(), name='tag-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
