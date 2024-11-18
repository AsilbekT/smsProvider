from django.urls import path
from .views import ReceiveSMSView, LoginAPIView, SMSSendStatisticView

urlpatterns = [
    path('api/sms/', ReceiveSMSView.as_view(), name='receive_sms'),
    path('mobile-sms/auth/login', LoginAPIView.as_view(), name='auth_login'),
    path('mobile-sms/statistic/send', SMSSendStatisticView.as_view(), name='sms-statistic-send'),
]
