from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Category, Product
from django.core.paginator import Paginator
from django.db.models import Q
from .cart import Cart

def dashboard(request):
    categories = Category.objects.all()
    cart = Cart(request)
    data = {
        'categories': categories,
        'cart_count': cart.get_count()
    }
    return render(request, 'shop/index.html', context=data)

def detail(request):
    cart = Cart(request)
    data = {
        'path': 'Product Details',
        'cart_count': cart.get_count()
    }
    return render(request, 'shop/details.html', context=data)

def shop_page(request):
    products = Product.objects.all()

    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(products, 8)
    cart = Cart(request)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)

    data = {
        "path": "Products",
        "products": page_products,
        'cart_count': cart.get_count()
    }
    return render(request, 'shop/shop.html', context=data)

def get_products_with_category(request, pk):
    products = Product.objects.filter(category_id=pk)
    category = get_object_or_404(Category, pk=pk)
    cart = Cart(request)
    data = {
        "path": "Category",
        "products": products,
        'cart_count': cart.get_count()
    }
    return render(request, 'shop/category-products.html', context=data)

def search_products(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    cart = Cart(request)
    data = {
        "path": "Search",
        "products": page_products,
        'cart_count': cart.get_count()
    }
    return render(request, 'shop/shop.html', context=data)