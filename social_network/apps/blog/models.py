from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .managers import BlogManager, CommentManager
from apps.core.utils import generate_unique_slug


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='posts', null=True, blank=True)
    slug = models.SlugField(unique_for_date='published')
    body = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    published = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    objects = models.Manager()
    blog = BlogManager()

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(Post, 'slug', self.slug, self.title)
        super(Post, self).save(*args, **kwargs)

    def last_comments(self):
        return reversed(self.comments.all()[:5])

    def get_absolute_url(self):
        return reverse_lazy('post_detail',
                            kwargs={'post': self.slug, 'year': self.published.year, 'month': self.published.month,
                                    'day': self.published.day})

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    objects = models.Manager()
    custom = CommentManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "#{}".format(self.pk)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
