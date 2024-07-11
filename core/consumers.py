import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from ..auth.models import CustomUser, UserStatus
from .models import ChatHistory, Message


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.connection_count = 0
    
    async def connect(self):
        print('Websocket Connected...')
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.connection_count += 1
            self.update_user_status(self.user.id, 'online')
            await self.channel_layer.group_add(
                f'{self.user.username}_inbox',
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        print('Websocket Disconnected...')
        self.connection_count -= 1
        if self.connection_count == 0:
            self.update_user_status(self.user.id, 'offline')
        await self.channel_layer.group_discard(
            f'{self.user.username}_inbox',
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        print('Message received from client')
        text_data_json = json.loads(text_data)
        received_data_type = text_data_json['type']

        if received_data_type == 'message':
            message = text_data_json['message']
            sender_user_id = text_data_json['user_id']
            receiver_user_id = text_data_json['receiver_id']
            group_id = text_data_json['group_id']

            user = await self.get_user(sender_user_id)
            receiver = await self.get_user(receiver_user_id)

            # For Personal message
            if not group_id:
                message_data = {
                    'user': user.username,
                    'message': message,
                }

                await self.channel_layer.group_send(
                    f'{receiver.username}_inbox',
                    {
                        'type': 'chat_message',
                        'message': message_data,
                    }
                )

                # Create chat_history if it's their first time chatting
                chat_history_name = f"{sender_user_id}_{receiver_user_id}"
                chat_history, created = await self.get_or_create_chat_history(chat_history_name)
                if created:
                    await self.add_users_to_chat_history(chat_history, user, receiver)

                await self.create_message(user, chat_history, message)

            # For Group message
            else:
                chat_history = await self.get_chat_history(group_id)
                async for group_user in chat_history.users.all():
                    if group_user != user:
                        message_data = {
                            'user': user.username,
                            'message': message,
                        }

                        await self.channel_layer.group_send(
                            f'{group_user.username}_inbox',
                            {
                                'type': 'chat_message',
                                'message': message_data,
                            }
                        )
                        await self.create_message(user, chat_history, message)
        elif received_data_type == 'updated_message_info':
            message_id = text_data_json['message_id']
            sender_user_id = text_data_json['user_id']
            receiver_user_id = text_data_json['receiver_id']


    async def chat_message(self, event):
        print("Chat message....")
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_chat_history(self, name):
        return ChatHistory.objects.get_or_create(name=name)

    @database_sync_to_async
    def add_users_to_chat_history(self, chat_history, user, receiver):
        chat_history.users.add(user, receiver)
        chat_history.save()

    @database_sync_to_async
    def create_message(self, user, chat_history, message):
        return Message.objects.create(user=user, chat_history=chat_history, message=message)

    @database_sync_to_async
    def get_chat_history(self, group_id):
        return ChatHistory.objects.get(id=group_id)

    @database_sync_to_async
    def update_user_status(self, user_id, status):
        UserStatus.objects.update_or_create(
            user_id=user_id, defaults={"status": status, "last_seen": datetime.now()}
        )

    @database_sync_to_async
    def update_message_info(self, message_id):
        message = 