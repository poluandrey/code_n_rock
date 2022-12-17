import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AppConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)('main_page', self.channel_name)
        self.accept()

    def disconnect(self, code):
        pass

    def new_file(self, event):
        self.send(text_data=json.dumps(event['text']))

