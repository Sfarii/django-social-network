from django.db import models
from django.db.models import Q


class ProfileQuerySet(models.QuerySet):

    def search_for_profiles(self, current_user, search_key_word):
        return self.select_related('user').\
            filter(Q(user__username__icontains=search_key_word) | Q(user__email__icontains=search_key_word)
                   | Q(user__first_name__icontains=search_key_word) | Q(user__last_name__icontains=search_key_word)
                   | Q(about_me__icontains=search_key_word) | Q(phone__icontains=search_key_word)
                   | Q(address__icontains=search_key_word)).\
            exclude(user__pk=current_user.pk)

    def get_profiles(self, current_user):
        return self.select_related('user').\
            exclude(user__pk=current_user.pk)

    def get_posts(self, user):
        return self.select_related('user').\
            prefetch_related('user__posts', 'user__posts__author').\
            filter(user__pk=user.pk).\
            get()

    def is_follower(self, user, follower):
        return self.select_related('user').\
            prefetch_related('followed', 'followed__follower', 'followed__followed').\
            filter(followed__follower__pk=user.pk, followed__followed__pk=follower.pk).\
            exists()

    def is_followed(self, user, followed):
        return self.select_related('user').\
            prefetch_related('followers', 'followers__follower', 'followers__followed').\
            filter(followers__follower__pk=followed.pk, followers__followed__pk=user.pk).\
            exists()

    def get_followers(self):
        return self.select_related('user').prefetch_related('followers', 'followers__follower', 'followers__followed')

    def get_followings(self):
        return self.select_related('user').prefetch_related('followers', 'followed__follower', 'followed__follower')


class ProfileManager(models.Manager):

    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def search_for_profiles(self, current_user, search_key_word):
        return self.get_queryset().search_for_profiles(current_user, search_key_word)

    def get_profiles(self, current_user):
        return self.get_queryset().get_profiles(current_user)

    def is_follower(self, user, follower):
        return self.get_queryset().is_follower(user, follower)

    def is_followed(self, user, followed):
        return self.get_queryset().is_followed(user, followed)

    def get_followers(self):
        return self.get_queryset().get_followers()

    def get_followings(self):
        return self.get_queryset().get_followings()

    def get_posts(self, user):
        return self.get_queryset().get_posts(user)
