from django.db import models
from django.db.models import Q


class RoomQuerySet(models.QuerySet):

    def get_room_for_participants(self, *participants):
        participants = list(participants)
        gen_query = Q(participants__pk=participants.pop(0).pk)
        for participant in participants:
            gen_query &= Q(participants__pk=participant.pk)
        return self.filter(gen_query)

    def get_rooms(self, user):
        return self.prefetch_related('participants', 'messages', 'messages__sender').\
            filter(participants__pk=user.pk).\
            order_by('created')

    def search_for_rooms(self, user, search_key_word):
        return self.prefetch_related('participants', 'messages', 'messages__sender').\
            filter(participants__pk=user.pk, name__icontains=search_key_word).\
            order_by('created')

    def get_room(self, user, slug):
        return self.prefetch_related('participants', 'messages', 'messages__sender').\
            filter(participants__pk=user.pk, slug=slug)


class RoomManager(models.Manager):

    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def get_rooms(self, user):
        return self.get_queryset().get_rooms(user)

    def search_for_rooms(self, user, search_key_word):
        return self.get_queryset().search_for_rooms(user, search_key_word)

    def get_room(self, user, slug):
        return self.get_queryset().get_room(user, slug)

    def get_room_for_participants(self, *participants):
        return self.get_queryset().get_room_for_participants(*participants)