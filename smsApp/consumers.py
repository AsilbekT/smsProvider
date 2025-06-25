from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SMSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from the query string
        token = self.scope['query_string'].decode().split("token=")[-1]

        # Validate the token (replace this with your token validation logic)
        if await self.validate_token(token):
            self.user_token = token
            # Add user to the "sms_group"
            await self.channel_layer.group_add("sms_group", self.channel_name)
            await self.accept()
        else:
            # Reject the connection if the token is invalid
            await self.close(code=403)

    async def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        await self.channel_layer.group_discard("sms_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handles incoming WebSocket messages.
        Echo back a parsed format.
        """
        try:
            data = json.loads(text_data)
            response_data = {
                "status": 200,
                "key": "received_message",
                "data": {
                    "token": self.user_token,
                    "received": data,
                }
            }
            await self.send(text_data=json.dumps(response_data))
        except Exception as e:
            # Handle errors gracefully
            error_response = {
                "status": 400,
                "key": "error",
                "message": str(e),
            }
            await self.send(text_data=json.dumps(error_response))

    async def sms_message(self, event):
        """
        Send a message to the WebSocket client.
        This method is called by other parts of your Django application.
        """
        phone = event['phone']
        text = event['text']

        # Prepare the response message
        response_data = {
            "status": 200,
            "key": "send_sms",
            "data": {
                "phone": phone,
                "text": text
            }
        }

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps(response_data))

    async def validate_token(self, token):
        """
        Custom token validation logic.
        Replace this with your actual validation logic (e.g., check the database).
        """
        # Placeholder: Check if token is non-empty and longer than 10 characters.
        # Replace with your own validation (e.g., checking against a database or a token service).
        return bool(token and len(token) > 10)

