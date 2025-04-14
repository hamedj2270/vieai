import socket
import socks
import requests
from django.conf import settings

class ProxyManager:
    def __init__(self):
        self.proxy_host = getattr(settings, 'PROXY_HOST', '127.0.0.1')
        self.proxy_port = getattr(settings, 'PROXY_PORT', 9050)
        self.original_socket = socket.socket

    def enable_proxy(self):
        """فعال‌سازی پروکسی"""
        socks.set_default_proxy(socks.SOCKS5, self.proxy_host, self.proxy_port)
        socket.socket = socks.socksocket

    def disable_proxy(self):
        """غیرفعال‌سازی پروکسی"""
        socket.socket = self.original_socket

    def make_request(self, url, method='GET', **kwargs):
        """انجام درخواست با پروکسی"""
        try:
            self.enable_proxy()
            response = requests.request(method, url, **kwargs)
            return response
        finally:
            self.disable_proxy()

class TelegramProxyBot:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.proxy_manager = ProxyManager()
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message):
        """ارسال پیام به تلگرام با استفاده از پروکسی"""
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = self.proxy_manager.make_request(url, method='POST', data=data)
            return response.json()
        except Exception as e:
            print(f"Error sending telegram message through proxy: {e}")
            return None

    def send_chat_message(self, user_message, bot_response):
        """ارسال پیام چت به تلگرام با استفاده از پروکسی"""
        message = f"""
🔔 پیام جدید از لایو چت:

👤 پیام کاربر:
{user_message}

🤖 پاسخ ربات:
{bot_response}
"""
        return self.send_message(message) 