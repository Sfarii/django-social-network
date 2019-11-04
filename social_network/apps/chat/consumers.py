from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.translation import gettext as _
import json

from .models import Room, Message


class AsyncChatConsumer(AsyncWebsocketConsumer):
    room = None
    sender = None
    room_group_name = None
    room_name = None

    async def connect(self):
        kwargs = self.scope['url_route']['kwargs']

        self.sender = self.scope["user"]
        self.room = await self.get_room(self.sender, kwargs['room_name'])

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': {
                    'type': 'on_connect',
                    'identifier': self.sender.pk,
                    'full_name': self.sender.get_full_name(),
                    'username': self.sender.username,
                    'avatar': self.sender.profile.get_avatar()
                }
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': {
                    'type': 'on_disconnect',
                    'identifier': self.sender.pk,
                    'full_name': self.sender.get_full_name(),
                    'username': self.sender.username,
                    'avatar': self.sender.profile.get_avatar()
                }
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Create the message
        message = await self.create_message(text_data_json)

        # Send the message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': {
                    'type': 'on_message',
                    'body': message.body,
                    'created': message.created.strftime("%b. %d, %Y %H:%M:%S"),
                    'username': self.sender.username,
                    'avatar': self.sender.profile.get_avatar()
                }
            }
        )

        await self.send_user_notification(message.body)

    async def broadcast(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    async def send_user_notification(self, message):
        """ Send notification to the user """

        title = _("%(user_full_name)s has send a message in room %(room_name)s") % {
            'user_full_name': self.sender.get_full_name(), 'room_name': self.room.name}

        participants_ids = self.room.get_participants_ids()
        participants_ids.remove(self.sender.pk)

        await self.channel_layer.group_send(
            'users_notifications',
            {
                'type': 'broadcast',
                'message': {
                    'username': self.sender.username,
                    'to': participants_ids,
                    'full_name': self.sender.get_full_name(),
                    'avatar': self.sender.profile.get_avatar(),
                    'title': title,
                    'description': message
                }
            }
        )

    @database_sync_to_async
    def get_room(self, sender, slug):
        return Room.details.get_room(sender, slug).get()

    @database_sync_to_async
    def get_room_participants(self):
        return self.room.participants.all()

    @database_sync_to_async
    def create_message(self, text_data_json):
        message = Message(sender=self.sender, room=self.room, body=text_data_json['message'])
        message.save()
        return message
