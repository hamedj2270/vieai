from django.shortcuts import render
from sites.models import Product


def home(request):
    products = Product.objects.filter(active=True)
    return render(request, "_base/_base.html", context={'products': products})