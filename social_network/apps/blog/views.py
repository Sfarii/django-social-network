from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin

from .models import Post, Comment, Like
from .forms import PostFrom, CommentFrom
from apps.core.mixins import LoginRequiredMixin, AjaxableResponseMixin


class PostDetailMixin(SingleObjectMixin):
    object = None

    def get_object(self, queryset=None):
        try:
            if self.object is None:
                self.object = Post.blog.get_post_and_comment(slug=self.kwargs.get('post'), year=self.kwargs.get('year'), month=self.kwargs.get('month'), day=self.kwargs.get('day')).get()
            return self.object
        except Post.DoesNotExist:
            raise Http404('No post matches the given query.')


class PostListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'blog/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        search_key_word = self.request.GET.get('search', None)
        if search_key_word is not None:
            return Post.blog.search_for_posts_and_comments(search_key_word)
        return Post.blog.get_posts_and_comments()


class PostCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Post
    form_class = PostFrom
    template_name = 'blog/post_create.html'
    success_message = 'Your post has been created successfully'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostDetailMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostFrom
    template_name = 'blog/post_update.html'
    success_message = 'Your post has been updated successfully'


class PostDetailView(LoginRequiredMixin, PostDetailMixin, ListView):
    model = Comment
    paginate_by = 5
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(object_list=self.get_queryset(), **kwargs)
        context['object'] = self.get_object()
        return context

    def get_queryset(self):
        return Comment.custom.get_post_comments(self.get_object())


class PostDeleteView(LoginRequiredMixin, PostDetailMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_index')
    success_message = 'Your post has been deleted successfully'
    template_name = 'blog/post_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)
