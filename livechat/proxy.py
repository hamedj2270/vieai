import requests
import socks
import socket
import time
from django.conf import settings
from .models import ChatMessage

class ProxyManager:
    def __init__(self):
        self.proxy_host = settings.PROXY_HOST
        self.proxy_port = settings.PROXY_PORT
        self.proxy_username = settings.PROXY_USERNAME
        self.proxy_password = settings.PROXY_PASSWORD

    def setup_proxy(self):
        socks.set_default_proxy(
            socks.SOCKS5,
            self.proxy_host,
            self.proxy_port,
            username=self.proxy_username,
            password=self.proxy_password
        )
        socket.socket = socks.socksocket

class TelegramProxyBot:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.last_update_id = 0
        # تنظیمات پروکسی (فقط برای محیط توسعه)
        self.use_proxy = getattr(settings, 'USE_PROXY', False)
        if self.use_proxy:
            self.proxy_host = settings.PROXY_HOST
            self.proxy_port = settings.PROXY_PORT
            self.proxy_username = settings.PROXY_USERNAME
            self.proxy_password = settings.PROXY_PASSWORD

    def send_message(self, message):
        """ارسال پیام به تلگرام"""
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        
        # فرمت‌بندی پیام برای تلگرام
        formatted_message = f"""
🔔 پیام جدید از لایو چت:

👤 پیام کاربر:
{message}

لطفاً پاسخ خود را ارسال کنید.
"""
        
        data = {
            'chat_id': self.chat_id,
            'text': formatted_message,
            'parse_mode': 'HTML'
        }
        
        try:
            if self.use_proxy:
                proxies = {
                    'http': f'socks5h://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                    'https': f'socks5h://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
                }
                response = requests.post(url, json=data, proxies=proxies)
            else:
                response = requests.post(url, json=data)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending message to Telegram: {str(e)}")
            return None

    def get_updates(self, timeout=30):
        """دریافت آخرین پیام‌های دریافتی از تلگرام"""
        url = f'https://api.telegram.org/bot{self.bot_token}/getUpdates'
        
        params = {
            'offset': self.last_update_id + 1,
            'timeout': timeout
        }
        
        try:
            if self.use_proxy:
                proxies = {
                    'http': f'socks5h://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                    'https': f'socks5h://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
                }
                response = requests.get(url, params=params, proxies=proxies)
            else:
                response = requests.get(url, params=params)
            
            response.raise_for_status()
            updates = response.json()
            
            if updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    self.last_update_id = update['update_id']
                    if 'message' in update and update['message']['chat']['id'] == int(self.chat_id):
                        return update['message']['text']
            
            return None
        except Exception as e:
            print(f"Error getting updates from Telegram: {str(e)}")
            return None

    def wait_for_response(self, max_attempts=6):
        """انتظار برای دریافت پاسخ از تلگرام"""
        for _ in range(max_attempts):
            response = self.get_updates(timeout=5)
            if response:
                return response
            time.sleep(5)  # انتظار 5 ثانیه قبل از تلاش مجدد
        return None

    def send_chat_message(self, message):
        """ارسال پیام چت به تلگرام و ذخیره پاسخ"""
        # ارسال پیام به تلگرام
        telegram_response = self.send_message(message)
        
        if telegram_response and telegram_response.get('ok'):
            # ذخیره پیام در دیتابیس
            chat_message = ChatMessage.objects.create(
                user_message=message,
                bot_response="",  # پاسخ خالی
                ip_address=None  # این مقدار در view تنظیم می‌شود
            )
            
            # انتظار برای دریافت پاسخ از تلگرام
            response_text = self.wait_for_response()
            if response_text:
                chat_message.telegram_response = response_text
                chat_message.is_responded = True
                chat_message.save()
                return response_text
            
            return ""  # پاسخ خالی
        
        return "متأسفانه در ارسال پیام مشکلی پیش آمده. لطفاً دوباره تلاش کنید." 