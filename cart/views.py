from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from myshop.models import Product
from .cart import Cart


def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product, quantity=quantity)
    return redirect("cart:detail")


@require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:detail")
