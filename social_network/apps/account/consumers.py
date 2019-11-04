from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import json
import traceback


class AsyncUserNotificationConsumer(AsyncWebsocketConsumer):
    BROADCASTS_TO_ALL = 'all'

    current_user = None
    room_group_name = None

    async def connect(self):
        self.current_user = self.scope["user"]
        self.room_group_name = "users_notifications"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            print(data)

            if data['type'] == 'offer':
                message = {'type': 'offer', 'offer': data['offer'], 'from': data['from'], 'to': data['to']}
            elif data['type'] == 'answer':
                message = {'type': 'answer', 'answer': data['answer'], 'from': data['from'], 'to': data['to']}
            elif data['type'] == 'call':
                message = {'type': 'call', 'callers': await self.get_caller_info(data['from']), 'from': data['from'], 'to': data['to']}
            elif data['type'] == 'candidate':
                message = {'type': 'candidate', 'candidate': data['candidate'], 'from': data['from'], 'to': data['to']}
            elif data['type'] == 'leave':
                message = {'type': 'leave', 'to': data['to']}
            else:
                message = {'type': 'error', 'message': 'Command not found: ' + data['type'], 'to': data['to']}

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'message': message
                }
            )
        except Exception as e:
            track = traceback.format_exc()
            print(track)

    async def send_message(self, event):
        # Send message to WebSocket
        try:
            data = dict(event['message'])
            broadcasts_to = data.pop('to', None)
            if broadcasts_to is not None and self.current_user.username in broadcasts_to:
                print(broadcasts_to)
                await self.send(text_data=json.dumps(data))
        except Exception as e:
            track = traceback.format_exc()
            print(track)

    async def broadcast(self, event):
        # Send message to WebSocket
        try:
            data = event['message']
            if ('exclude' in data and self.current_user.pk not in data['exclude']) or ('to' in data and self.current_user.pk in data['to']):
                data.update({'type': 'notification'})
                await self.send(text_data=json.dumps(data))
        except Exception as e:
            track = traceback.format_exc()
            print(track)

    @database_sync_to_async
    def get_caller_info(self, callers_username):
        users = User.objects.prefetch_related('profile').filter(username__in=callers_username).all()
        return [{'avatar': user.profile.get_avatar(), 'full_name': user.get_full_name()} for user in users]