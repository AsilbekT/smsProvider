from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SMSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sms_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sms_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Handle incoming data from WebSocket, if any
        #
        pass

    # Handle messages from Django view
    async def sms_message(self, event):
        phone = event['phone']
        text = event['text']

        # Prepare the JSON data to send to the client
        response_data = {
            "status": 200,
            "key": "send_sms",
            "data": {
                "phone": phone,
                "text": text
            }
        }

        # Send message to WebSocket client
        await self.send(text_data=json.dumps(response_data))