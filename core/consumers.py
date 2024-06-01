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
    self.room_group_name  = self.scope['url_route']['kwargs']['group_name']
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name,
    )
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
    user_id = text_data_json['user_id']
    chat_history_id = text_data_json['chat_history_id']
    user = User.objects.get(id=user_id)
    chat_history = ChatHistory.objects.get(id=chat_history_id)

    message_instance = Message.objects.create(
      user=user,
      chat_history=chat_history,
      message=message
    )

    message_data = {
      'id': message_instance.id,
      'user': user.username,
      'message': message_instance.message,
      'sent_timestamp': message_instance.sent_timestamp.isoformat()
    }

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