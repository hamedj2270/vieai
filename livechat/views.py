from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ChatMessage
from .proxy import TelegramProxyBot

@api_view(['POST'])
@permission_classes([AllowAny])
def send_message(request):
    """پردازش پیام‌های چت و ارسال به تلگرام"""
    message = request.data.get('message', '')
    if not message:
        return Response({'error': 'پیام نمی‌تواند خالی باشد'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # ارسال پیام به تلگرام با استفاده از پروکسی
        telegram_bot = TelegramProxyBot()
        response = telegram_bot.send_chat_message(message)
        
        # به‌روزرسانی IP آدرس در دیتابیس
        chat_message = ChatMessage.objects.latest('id')
        chat_message.ip_address = request.META.get('REMOTE_ADDR')
        chat_message.save()
        
        return Response({
            'success': True, 
            'response': response,
            'message_id': chat_message.id
        })
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        return Response({
            'success': False,
            'error': 'خطا در ارسال پیام. لطفاً دوباره تلاش کنید.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_telegram_response(request, message_id):
    """دریافت پاسخ تلگرام برای یک پیام خاص"""
    try:
        chat_message = ChatMessage.objects.get(id=message_id)
        if chat_message.telegram_response:
            return Response({
                'success': True,
                'response': chat_message.telegram_response
            })
        return Response({
            'success': False,
            'message': 'هنوز پاسخی دریافت نشده است'
        })
    except ChatMessage.DoesNotExist:
        return Response({
            'success': False,
            'message': 'پیام یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)
