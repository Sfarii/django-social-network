from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .managers import RoomManager
from apps.core.utils import generate_unique_slug


class Room(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.FileField(upload_to='rooms', default='rooms/avatar-chat.svg', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User)

    objects = models.Manager()
    details = RoomManager()

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(Room, 'slug', self.slug, self.name)
        super(Room, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('detail_room', kwargs={'slug': self.slug})

    def get_participants_ids(self):
        return list(self.participants.values_list('pk', flat=True))

    def get_last_message(self):
        return self.messages.latest('created')

    def __str__(self):
        return self.name


class Message(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE, related_name='messages')

    def __str__(self):
        return "#{}".format(self.pk)

    class Meta:
        ordering = ('-created', )