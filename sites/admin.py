from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_filter = ['order']
    search_fields = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'active']
    list_filter = ['category', 'active']
    search_fields = ['title', 'description', 'tags']

    class Meta:
        model = Product

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

