from django.urls import path, re_path
from .views import PostListView, PostCreateView, PostDeleteView, PostUpdateView, PostDetailView


urlpatterns = (
    path('posts/', PostListView.as_view(), name='post_index'),
    path('post/create', PostCreateView.as_view(), name='post_create'),

    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/details', PostDetailView.as_view(), name='post_detail')
)