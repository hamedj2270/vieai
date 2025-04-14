from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'image', 'order', 'is_active', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'link', 'category', 'category_name', 
                 'link_preview_image', 'link_preview_title', 'link_preview_description',
                 'created_at', 'updated_at']

    def validate_category_id(self, value):
        try:
            models.Category.objects.get(id=value)
        except models.Category.DoesNotExist:
            raise serializers.ValidationError("دسته‌بندی مورد نظر یافت نشد")
        return value
