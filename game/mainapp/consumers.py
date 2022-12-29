import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["type"]

        # Send message to room group
        if message_type == "enter":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "enter", "message": message}
            )
        elif message_type == "attack":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "attack", "message": message}
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def enter(self, event):
        message = event["message"]
        message_type = event["type"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": message_type, "message": message}))

    def attack(self, event):
        message = event["message"]
        message_type = event["type"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": message_type, "message": message}))