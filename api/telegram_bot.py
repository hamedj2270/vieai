import requests
from django.conf import settings

class TelegramBot:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message):
        """ارسال پیام به تلگرام"""
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Error sending telegram message: {e}")
            return None

    def send_chat_message(self, user_message, bot_response):
        """ارسال پیام چت به تلگرام"""
        message = f"""
🔔 پیام جدید از لایو چت:

👤 پیام کاربر:
{user_message}

🤖 پاسخ ربات:
{bot_response}
"""
        return self.send_message(message) 