import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.models import User
from .models import ChatHistory, Message

class ChatConsumer(WebsocketConsumer):
   
  def __init__(self, *args, **kwargs):
    super().__init__(args, kwargs)
    self.room_name = None
    self.room_group_name = None
    self.room = None
    
  def websocket_connect(self,event):
    print('Websocket Connected...',event)
    print(self.channel_name)
    self.user = self.scope['user']
    if self.user.is_authenticated:
      user_groups = ChatHistory.objects.filter(users=self.user)
      if user_groups is not None:
       for group in user_groups:
        self.room_group_name = group.name
        async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
      )
      self.accept()
    else:
      self.close()

  def websocket_disconnect(self, close_code):
    print('Websocket Disconnected...')
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name,
    )

  def receive(self, text_data=None, bytes_data=None):
    print('Message received from client')
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    sender_user_id = text_data_json['user_id']
    receiver_user_id = text_data_json['receiver_id']
    user = User.objects.get(id=sender_user_id)
    receiver = User.objects.get(id=receiver_user_id)

    # Create chat_history if it's their first time chatting
    chat_history_name = f"{sender_user_id}_{receiver_user_id}"
    chat_history, created = ChatHistory.objects.get_or_create(name=chat_history_name)
    if created:
      self.room_group_name = str(chat_history.name)
      chat_history.users.add(user, receiver)
      chat_history.save()
      # Add channel to the group
      print(self.room_group_name)
      print(type(self.room_group_name))
      async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
      )
    else:
      self.room_group_name = str(chat_history.name)
      
    message_data = {
      'user': user.username,
      'message': message,
    }

    # send chat message event to the room
    print("Chat message....",message_data)
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message_data,
      }
    )
    message_instance = Message.objects.create(
      user=user,
      chat_history = chat_history,
      message=message
    )

  def chat_message(self, event):
    print("Chat message....")
    self.send(text_data=json.dumps(event))