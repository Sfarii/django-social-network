from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import date
from hashlib import md5

from .managers import ProfileManager


class Profile(models.Model):
    LANGUAGE_CHOICES = (
        ('fr-FR', _('French')),
        ('en-GB', _('English'))
    )
    avatar = models.FileField(verbose_name='Avatar', upload_to='avatars', null=True, blank=True)
    about_me = models.TextField(max_length=500, null=True)
    phone = models.CharField(max_length=32, null=True)
    address = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    objects = models.Manager()
    manager = ProfileManager()

    def get_avatar(self, size=100):
        if self.avatar:
            return self.avatar.url
        email_hash = md5(self.user.email.lower().encode('utf-8')).hexdigest()
        return 'https://secure.gravatar.com/avatar/{hash}?s={size}&d={default}&r={rating}'. \
            format(hash=email_hash, size=size, default='identicon', rating='g')

    def age(self):
        return int(abs(self.birthday - date.today()).days / 365) if self.birthday is not None else None

    def get_absolute_url(self):
        return reverse_lazy('profile', kwargs=dict(username=self.user.username))

    def __str__(self):
        return self.user.get_full_name()


class Follow(models.Model):

    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followed')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now=True)