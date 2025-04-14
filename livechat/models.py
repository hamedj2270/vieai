from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    user_message = models.TextField(verbose_name='پیام کاربر')
    bot_response = models.TextField(verbose_name='پاسخ ربات')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='آدرس IP')
    telegram_response = models.TextField(null=True, blank=True, verbose_name='پاسخ تلگرام')
    is_responded = models.BooleanField(default=False, verbose_name='پاسخ داده شده')

    class Meta:
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام‌های چت'
        ordering = ['-created_at']

    def __str__(self):
        return f"پیام از {self.ip_address} - {self.created_at}"
