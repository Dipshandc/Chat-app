import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import django
django.setup() 
from authentication.models import CustomUser, UserStatus
from django.utils import timezone
from .models import ChatHistory, Message
from .serializers import MessageSerializer, UserStatusSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    online_count = {}

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.user = None

    
    async def connect(self):
        print('Websocket Connected...')
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()

            await self.channel_layer.group_add(
                f'{self.user.username}_inbox',
                self.channel_name
                )
            
            status_obj = await self.update_user_status(self.user.id, 'online')
            serialized_status = await self.serialize_status(status_obj)
            
            
            if serialized_status:
                if self.user.id in self.online_count:
                    self.online_count[self.user.id] += 1
                else:
                    self.online_count[self.user.id] = 1
                users = await self.get_user_list(self.user)
                for user in users:
                    await self.channel_layer.group_send(
                        f'{user}_inbox',
                        {
                            'type': 'user_status_update',
                            'message': serialized_status.data,
                        }
                    )
            else:
                print('Error updating user status')
                
        else:
            await self.close()

    async def disconnect(self, close_code):
        print(f'Websocket Disconnected with code: {close_code}')
        await self.channel_layer.group_discard(
            f'{self.user.username}_inbox',
            self.channel_name,
        )
        if self.user.id in self.online_count:
            self.online_count[self.user.id] -= 1
            if self.online_count[self.user.id] == 0:
                status_obj = await self.update_user_status(self.user.id, 'offline')
                serialized_status = await self.serialize_status(status_obj)
                users = await self.get_user_list(self.user)
                for user in users:
                 await self.channel_layer.group_send(
                     f'{user}_inbox',
                        {
                            'type': 'user_status_update',
                            'message': serialized_status.data,
                        }
                    )
                del self.online_count[self.user.id]
                

    async def receive(self, text_data=None, bytes_data=None):
        print('Message received from client')
        text_data_json = json.loads(text_data)
        print(text_data_json)
        received_data_type = text_data_json['type']

        if received_data_type == 'message':
            message = text_data_json['message']
            sender_user_id = self.user.id
            receiver_user_id = text_data_json['receiver_id']
            group_id = text_data_json['group_id']

            user = await self.get_user(sender_user_id)
            receiver = await self.get_user(receiver_user_id)

            # For Personal message

            if not group_id:
                # Create chat_history if it's their first time chatting
                chat_history_name = f"{min(sender_user_id,receiver_user_id)}_{max(sender_user_id,receiver_user_id)}"
                chat_history, created = await self.get_or_create_chat_history(chat_history_name)
                if created:
                    await self.add_users_to_chat_history(chat_history, user, receiver)
                message_obj =  await self.create_message(user, chat_history, message)
                serialize_message = await self.serialize_message(message_obj)
                message_data = serialize_message.data


                await self.channel_layer.group_send(
                    f'{receiver.username}_inbox',
                    {
                        'type': 'chat_message',
                        'message': message_data,
                    }
                )
                await self.channel_layer.group_send(
                    f'{user.username}_inbox',
                    {
                        'type': 'chat_message',
                        'message': message_data,
                    }
                )
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
            receiver_user_id = text_data_json['receiver_id']
            receiver = await self.get_user(receiver_user_id)
            updated_message_info_type = text_data_json['updated_message_info_type']
            if updated_message_info_type == 'seen':
                message_obj =  await self.update_message_seen_status(message_id)
                serialize_message = await self.serialize_message(message_obj)
                message_data = serialize_message.data

                await self.channel_layer.group_send(
                    f'{receiver.username}_inbox',
                    {
                        'type': 'chat_message_info',
                        'message': message_data,
                    }
                )
            else:
                message_obj =  await self.update_message_delivered_status(message_id)
                serialize_message = await self.serialize_message(message_obj)
                message_data = serialize_message.data

                await self.channel_layer.group_send(
                    f'{receiver.username}_inbox',
                    {
                        'type': 'chat_message_info',
                        'message': message_data,
                    }
                )


    async def chat_message(self, event):
        print("Chat message....")
        await self.send(text_data=json.dumps(event))

    async def chat_message_info(self, event):
        print("Chat message info changed....")
        await self.send(text_data=json.dumps(event))
    
    async def user_status_update(self, event):
        print("User status updatedd....")
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
    def serialize_message(self,message_obj):
        return MessageSerializer(message_obj)
    
    @database_sync_to_async
    def serialize_status(self,status_obj):
        return UserStatusSerializer(status_obj)

    @database_sync_to_async
    def get_chat_history(self, group_id):
        return ChatHistory.objects.get(id=group_id)

    @database_sync_to_async
    def update_user_status(self, user_id, status):
        user_status = UserStatus.objects.get(
            user_id=user_id)
        user_status.status = status
        user_status.last_seen=timezone.now()
        user_status.save()
        return user_status
    
    @database_sync_to_async
    def update_message_seen_status(self, message_id):
        message =  Message.objects.get(id=message_id)
        message.seen_timestamp = timezone.now()
        return message.save()

    @database_sync_to_async
    def update_message_delivered_status(self, message_id):
        message =  Message.objects.get(id=message_id)
        message.delivered_timestamp = timezone.now()
        return message.save()
    
    @database_sync_to_async
    def get_user_list(self,user):
        user_list = []
        users = CustomUser.objects.exclude(id=user.id).exclude(is_superuser=True)
        for user in users:
            user_list.append(user.username)
        return user_list
