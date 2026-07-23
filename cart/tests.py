from django.test import TestCase
from django.urls import reverse

from myshop.models import Category, Product


class CartTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Кеды', slug='kedy')
        cls.product = Product.objects.create(
            category=cls.category,
            name='Товар в корзину',
            slug='tovar-v-korzinu',
            description='Описание для корзины.',
            price='2599.00',
            is_available=True,
        )

    def test_cart_add_and_remove(self):
        add_url = reverse('cart:add', kwargs={'product_id': self.product.id})
        response = self.client.post(add_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)
        cart_response = self.client.get(reverse('cart:detail'))
        self.assertEqual(cart_response.status_code, 200)
        self.assertContains(cart_response, self.product.name)
        self.assertContains(cart_response, '2')
        self.assertContains(cart_response, '5198.00')

        remove_url = reverse('cart:remove', kwargs={'product_id': self.product.id})
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)
        cart_response = self.client.get(reverse('cart:detail'))
        self.assertEqual(cart_response.status_code, 200)
        self.assertNotContains(cart_response, self.product.name)

    def test_cart_detail_page_empty(self):
        response = self.client.get(reverse('cart:detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Корзина пуста')
