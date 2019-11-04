from django.db import models
from django.db.models import Q, Prefetch, Count, Subquery, OuterRef
from django.apps import apps


class BlogQuerySet(models.QuerySet):

    def get_posts_and_comments(self):
        comment_model = apps.get_model('blog', 'Comment')
        comment_queryset = comment_model.objects.select_related('author').prefetch_related('author__profile').annotate(
            likes_length=Count('likes', distinct=True)).filter(pk__in=Subquery(
            comment_model.objects.filter(post__pk=OuterRef('post__pk')).values_list('pk', flat=True)[:5])).all()

        return self.select_related('author'). \
            prefetch_related(Prefetch('comments', queryset=comment_queryset, to_attr='comment_list'),
                             'author__profile'). \
            filter(status='published'). \
            order_by('-published'). \
            annotate(likes_length=Count('likes', distinct=True), comments_length=Count('comments', distinct=True))

    def search_for_posts_and_comments(self, search_key_word):
        comment_model = apps.get_model('blog', 'Comment')
        comment_queryset = comment_model.objects.select_related('author').prefetch_related('author__profile').annotate(
            likes_length=Count('likes', distinct=True)).filter(pk__in=Subquery(
            comment_model.objects.filter(post__pk=OuterRef('post__pk')).values_list('pk', flat=True)[:5])).all()

        return self.select_related('author'). \
            prefetch_related(Prefetch('comments', queryset=comment_queryset, to_attr='comment_list'),
                             'author__profile'). \
            filter(Q(title__icontains=search_key_word) | Q(body__icontains=search_key_word)
                   | Q(comments__body__icontains=search_key_word), status='published'). \
            order_by('-published'). \
            annotate(likes_length=Count('likes', distinct=True), comments_length=Count('comments', distinct=True))

    def get_post_and_comment(self, slug, year, month, day):
        return self.filter(slug=slug, published__year=year, published__month=month, published__day=day). \
            select_related('author'). \
            prefetch_related('author__profile').\
            annotate(likes_length=Count('likes', distinct=True), comments_length=Count('comments', distinct=True))

    def get_post(self, pk):
        return self.select_related('author'). \
            prefetch_related('author__profile', 'likes', 'likes__author'). \
            filter(pk=pk)


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def get_posts_and_comments(self):
        return self.get_queryset().get_posts_and_comments()

    def search_for_posts_and_comments(self, search_key_word):
        return self.get_queryset().search_for_posts_and_comments(search_key_word)

    def get_post_and_comment(self, slug, year, month, day):
        return self.get_queryset().get_post_and_comment(slug, year, month, day)

    def get_post(self, pk):
        return self.get_queryset().get_post(pk)


class CommentQuerySet(models.QuerySet):

    def get_post_comments(self, post):
        return self.select_related('author', 'post').\
            prefetch_related('author__profile').\
            annotate(likes_length=Count('likes', distinct=True)).\
            order_by('-created').\
            filter(post__pk=post.pk)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def get_post_comments(self, post):
        return self.get_queryset().get_post_comments(post)