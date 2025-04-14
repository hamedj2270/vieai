from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .proxy import TelegramProxyBot

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_message(request):
    """پردازش پیام‌های چت و ارسال به تلگرام"""
    message = request.data.get('message', '')
    if not message:
        return Response({'error': 'پیام نمی‌تواند خالی باشد'}, status=status.HTTP_400_BAD_REQUEST)
    
    # پاسخ‌های پیش‌فرض ربات
    responses = [
        "ممنون از پیام شما. به زودی با شما تماس خواهیم گرفت.",
        "سوال خوبی پرسیدید. اجازه دهید بررسی کنم.",
        "برای اطلاعات بیشتر می‌توانید با پشتیبانی تماس بگیرید.",
        "لطفاً سوال خود را با جزئیات بیشتری مطرح کنید."
    ]
    bot_response = responses[0]  # یا می‌توانید از یک الگوریتم پیچیده‌تر استفاده کنید
    
    # ارسال پیام به تلگرام با استفاده از پروکسی
    telegram_bot = TelegramProxyBot()
    telegram_bot.send_chat_message(message, bot_response)
    
    return Response({'response': bot_response})

def home(request):
    """نمایش صفحه اصلی با دسته‌بندی‌ها و محصولات"""
    categories = Category.objects.filter(is_active=True)
    selected_category = request.GET.get('category')
    
    if selected_category:
        products = Product.objects.filter(category__slug=selected_category)
    else:
        products = Product.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'query': request.GET.get('q', '')
    }
    return render(request, '_base/_base.html', context)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(active=True)
        return queryset

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        product = self.get_object()
        product.active = not product.active
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=True)
    def increment_views(self, request, pk=None):
        product = self.get_object()
        product.views += 1
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order']
    ordering = ['order', 'name']

    @action(detail=True)
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
