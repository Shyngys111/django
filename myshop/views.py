from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_list(request):
    """Главная страница — все доступные товары"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(
        request,
        "products/product_list.html",
        {"products": products, "categories": categories},
    )


def product_detail(request, slug):
    """Страница одного товара"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, "products/product_detail.html", {"product": product})


def category_products(request, slug):
    """Товары одной категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    return render(
        request,
        "products/product_list.html",
        {"products": products, "categories": Category.objects.all(), "current_category": category},
    )