from django.http import Http404
from django.views.generic import ListView, CreateView, DeleteView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Room, Message
from .forms import RoomForm
from apps.core.mixins import LoginRequiredMixin


class CreateRoomView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Room
    template_name = 'chat/room_create.html'
    success_message = 'Your room has been created successfully'

    def get_form(self, form_class=None):
        return RoomForm(current_user=self.request.user, **self.get_form_kwargs())


class RoomListView(ListView, LoginRequiredMixin):
    model = Room
    paginate_by = 9
    template_name = 'chat/room_list.html'
    search_key_word = None

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['search_key_word'] = self.search_key_word
        return context

    def get_queryset(self):
        self.search_key_word = self.request.GET.get('search', None)
        if self.search_key_word is not None:
            return Room.details.search_for_rooms(self.request.user, self.search_key_word)
        return Room.details.get_rooms(self.request.user)


class RoomDetailView(ListView, LoginRequiredMixin):
    template_name = 'chat/room_detail.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(object_list=self.get_queryset(), **kwargs)
        context['current_room'] = self.get_current_room()
        context['message_list'] = reversed(self.object_list)
        return context

    def get_current_room(self):
        try:
            return Room.details.get_room(self.request.user, self.kwargs.get('slug', None)).get()
        except Room.DoesNotExist:
            raise Http404('No Rooms matches the given query.')

    def get_queryset(self):
        return Message.objects.select_related('room', 'sender').filter(room__slug=self.kwargs.get('slug', None))


class DeleteRoomView(DeleteView, LoginRequiredMixin):
    model = Room
    success_url = reverse_lazy('list_rooms')
    template_name = 'chat/room_confirm_delete.html'


class CreateRoomForUserView(RedirectView, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        return super(CreateRoomForUserView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        participant = self.get_participant()
        room_name = "{} & {}".format(self.request.user.get_full_name(), participant.get_full_name())
        room_slug = "{}-{}".format(self.request.user.username, participant.username)
        room, created = Room.details.get_room_for_participants(self.request.user, participant).get_or_create(slug=room_slug, name=room_name)
        if created:
            print(room.slug)
            messages.add_message(self.request, messages.INFO, _('New room has been created successfully.'))
            room.participants.add(self.request.user, participant)
            room.save()
        return room.get_absolute_url()

    def get_participant(self):
        return User.objects.get(username__exact=self.kwargs.get('username', None))