from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .serializers import SMSStatisticSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                # Optionally handle and save device and firebase token details here
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'status': 1,
                    'name': "asdfa",
                    'message': "asdfasdf",
                    'step': 4,
                    'data': {
                        "id": user.pk,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "device_id": serializer.validated_data.get('device_id', ""),
                        "firebase_token": serializer.validated_data.get('firebase_token', ""),
                        "device_name": serializer.validated_data.get('device_name', ""),
                        'auth_key': token.key,
                        'username': user.username
                    }
                })
            else:
                raise AuthenticationFailed('Invalid username/password.')
        else:
            return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ReceiveSMSView(View):
    def post(self, request, *args, **kwargs):
        # Parse the incoming JSON data
        try:
            sms_data = json.loads(request.body)
            phone = sms_data.get('phone', '')  
            text = sms_data.get('text', '') 
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"status": "error", "message": "Invalid data sent"}, status=400)

        # Send the structured message to WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "sms_group",  # This should match the group name used in your consumer
            {
                "type": "sms.message",
                "phone": phone,
                "text": text
            }
        )

        return JsonResponse({"status": 200, "key": "send_sms", "data": {"phone": phone, "text": text}})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "error", "message": "GET method not allowed"}, status=405)
    

class SMSSendStatisticView(APIView):
    def post(self, request):
        serializer = SMSStatisticSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(        {
                    'success': True,
                    'status': 1,
                    'name': "sms",
                    'message': "delivered",
                    'step': 1,
                    'data': serializer.data
                }, status=200)

        return Response(serializer.errors, status=400)
