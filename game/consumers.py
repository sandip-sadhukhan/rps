import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'
        """
        # steps
            1. Check room is created or not?
            2. If not created, then create new room and join the user
            3. If created, check room is full or not?
            4. If room is full, then show the error message
            5. If not full, then join the user
        """
        room, new = Room.objects.get_or_create(
            id=self.room_name
        )
        self.room = room
        if not self.room.is_full():
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            self.room.joinUser()

    def disconnect(self, close_code):
        """
        # steps
        1. Remove room
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'data': {
                    "type": "deleteRoom"
                }
            }
        )
        self.room.delete()

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        if(data.get('type') == 'saveTurn'):
            self.room.saveTurn(data['userId'], data['turn'])
        else:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'data': data
                }
            )

    # Receive message from room group
    def send_message(self, event):
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))
