from django.db import models
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(unique=True, verbose_name='نامک')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=50, blank=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='نام سایت')
    description = models.TextField(verbose_name='توضیحات')
    link = models.CharField(max_length=200, verbose_name='لینک')
    image = models.ImageField(verbose_name='عکس محصول', upload_to='images/', null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name='فعال/ غیرفعال')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته‌بندی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    views = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    tags = models.CharField(max_length=200, blank=True, verbose_name='برچسب‌ها')

    class Meta:
        verbose_name = 'سایت'
        verbose_name_plural = 'سایت ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/product/{self.id}/{self.title.replace(' ', '-')}"

    def get_product_image(self):
        return self.image.url if self.image else ''