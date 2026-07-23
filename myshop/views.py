from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request):
    """Главная страница — список доступных товаров, поиск и фильтрация"""
    search_query = request.GET.get("q", "").strip()
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
        },
    )


def product_detail(request, slug):
    """Страница одного товара"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, "products/product_detail.html", {"product": product})


def category_products(request, slug):
    """Товары одной категории"""
    category = get_object_or_404(Category, slug=slug)
    search_query = request.GET.get("q", "").strip()
    products = Product.objects.filter(category=category, is_available=True)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "current_category": category,
            "search_query": search_query,
        },
    )
