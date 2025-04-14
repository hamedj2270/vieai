from django.urls import path
from . import views

app_name = 'livechat'

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('get_response/<int:message_id>/', views.get_telegram_response, name='get_telegram_response'),
] 