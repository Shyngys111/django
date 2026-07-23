from decimal import Decimal
from django.conf import settings
from myshop.models import Product


class Cart:
    """
    Класс-обёртка над сессией для работы с корзиной.
    """

    def __init__(self, request):
        """Инициализация корзины из сессии"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавить товар или обновить количество"""
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "product_name": product.name,
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        """Пометить сессию как изменённую"""
        self.session.modified = True

    def remove(self, product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор товаров в корзине с подгрузкой объектов Product из БД.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart_item = cart[str(product.id)]
            cart_item["product"] = product
            cart_item["total_price"] = Decimal(cart_item["price"]) * cart_item["quantity"]
            yield cart_item

    def __len__(self):
        """Общее количество товаров (сумма quantity)"""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        """Очистить корзину"""
        del self.session[settings.CART_SESSION_ID]
        self.save()