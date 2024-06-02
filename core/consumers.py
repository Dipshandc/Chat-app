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
    self.scope
    self.accept()

  def websocket_disconnect(self, close_code):
    print('Websocket Disconnected...')
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name,
    )

  def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    sender_user_id = text_data_json['user_id']
    receiver_user_id = text_data_json['receiver_id']
    user = User.objects.get(id=sender_user_id)
    receiver = User.objects.get(id=receiver_user_id)

    # Create chat_history if its their first time chati"6a5b53b8-2605-4297-85b8-701e5452fee6"ng
    chat_history = ChatHistory.objects.filter(name=f"{sender_user_id}:{receiver_user_id}")

    if chat_history is None:
      chat_history = ChatHistory.objects.create(name=f"{sender_user_id}:{receiver_user_id}")
      chat_history.users = user
      chat_history.users = receiver
      chat_history = chat_history.save()
      chat_history = ChatHistory.objects.filter(name=f"{sender_user_id}:{receiver_user_id}")
      async_to_sync(self.channel_layer.group_add)(
        str(chat_history.name),
        self.channel_name
      )


    message_instance = Message.objects.create(
      user=user,
      chat_history = ChatHistory.objects.filter(name=f"{sender_user_id}:{receiver_user_id}"),
      message=message
    )

    message_data = {
      'id': message_instance.id,
      'user': user.username,
      'message': message_instance.message,
      'sent_timestamp': message_instance.sent_timestamp.isoformat()
    }

    # Adds sender and receiver/receivers to same group
    

    # send chat message event to the room
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message_data,
      }
    )

  def chat_message(self, event):
    self.send(text_data=json.dumps(event))