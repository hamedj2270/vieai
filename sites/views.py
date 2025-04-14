from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

def home(request):
    # Get search query
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    # Base queryset
    products = Product.objects.filter(active=True)
    
    # Apply search if query exists
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Apply category filter if selected
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Get all categories for the filter
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug
    }
    return render(request, 'home.html', context)

# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     return render(request, 'product_detail.html', {'product': product})
