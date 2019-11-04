from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.translation import gettext as _
import json
import traceback

from .models import Post, Comment, Like


class AsyncPostConsumer(AsyncWebsocketConsumer):
    user = None
    room_group_name = None

    actions = dict(create_comment='create_comment', like_comment='like_comment', like_post='like_post')

    async def connect(self):
        self.user = self.scope["user"]

        self.room_group_name = 'posts_notifications'

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
            text_data_json = json.loads(text_data)
            comment = None
            post = None
            action = text_data_json.get('action', None)
            if action == self.actions.get('create_comment'):
                comment, post = await self.create_comment(text_data_json)
            elif action == self.actions.get('like_comment'):
                comment, post = await self.add_comment_like(text_data_json)
            elif action == self.actions.get('like_post'):
                post = await self.add_post_like(text_data_json)

            if comment is not None:
                message = {
                    'body': comment.body,
                    'action': action,
                    'comment_pk': comment.pk,
                    'post_pk': post.pk,
                    'comment_likes': comment.likes.count(),
                    'post_comments': post.comments.count(),
                    'created': comment.created.strftime("%b. %d, %Y %H:%M:%S"),
                    'full_name': self.user.get_full_name(),
                    'username': self.user.username,
                    'avatar': self.user.profile.get_avatar()
                }
            else:
                message = {
                    'action': action,
                    'post_pk': post.pk,
                    'post_likes': post.likes.count(),
                    'full_name': self.user.get_full_name(),
                    'username': self.user.username,
                    'avatar': self.user.profile.get_avatar()
                }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            await self.send_user_notification(action, post)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def add_comment_like(self, text_data_json):
        comment = self.get_comment(text_data_json['comment_pk'])
        like, created = Like.objects.get_or_create(author=self.user, comment=comment)
        if not created:
            like.delete()
        comment.refresh_from_db()
        return comment, comment.post

    @database_sync_to_async
    def create_comment(self, text_data_json):
        post = self.get_post(text_data_json['post_pk'])
        comment = Comment(author=self.user, post=post, body=text_data_json['message'])
        comment.save()
        return comment, post

    @database_sync_to_async
    def add_post_like(self, text_data_json):
        post = self.get_post(text_data_json['post_pk'])
        like, created = Like.objects.get_or_create(author=self.user, post=post)
        if not created:
            like.delete()
        post.refresh_from_db()
        return post

    def get_comment(self, comment_pk):
        return Comment.objects.get(pk=comment_pk)

    def get_post(self, post_pk):
        return Post.blog.get_post(post_pk).get()

    async def send_user_notification(self, action, post):
        """ Send notification to the user """

        if action == self.actions.get('create_comment'):
            title = _("%(full_name)s comment on the post %(post_title)s") % {'full_name': self.user.get_full_name(), 'post_title': post.title}
            description = _("Be the first to comment")
        elif action == self.actions.get('like_comment'):
            title = _("%(full_name)s has like a comment on the post %(post_title)s") % {'full_name': self.user.get_full_name(), 'post_title': post.title}
            description = _("Let's take a look")
        else:
            title = _("%(full_name)s has like the post %(post_title)s") % {'full_name': self.user.get_full_name(), 'post_title': post.title}
            description = _("Let's take a look")

        await self.channel_layer.group_send(
            'users_notifications',
            {
                'type': 'broadcast',
                'message': {
                    'username': self.user.username,
                    'exclude': (self.user.pk, ),
                    'full_name': self.user.get_full_name(),
                    'avatar': self.user.profile.get_avatar(),
                    'title': title,
                    'description': description
                }
            }
        )