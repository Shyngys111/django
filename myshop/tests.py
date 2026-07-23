import tempfile
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product


class ProductViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Кроссовки', slug='krossovki')
        cls.product = Product.objects.create(
            category=cls.category,
            name='Тестовый товар',
            slug='testovy-tovar',
            description='Описание тестового товара.',
            price='3999.99',
            is_available=True,
        )
        cls.other_product = Product.objects.create(
            category=cls.category,
            name='Дополнительный товар',
            slug='dopolnitelnyy-tovar',
            description='Другой товар.',
            price='2499.50',
            is_available=True,
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.other_product.name)
        self.assertContains(response, self.category.name)

    def test_category_products_view(self):
        response = self.client.get(reverse('products:category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.other_product.name)
        self.assertContains(response, 'active')

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, str(self.product.price))
        self.assertContains(response, 'Добавить в корзину')

    def test_product_image_url_uses_media_url(self):
        temp_dir = tempfile.mkdtemp()
        try:
            with override_settings(MEDIA_ROOT=temp_dir):
                image_content = SimpleUploadedFile(
                    'test_image.jpg', b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg'
                )
                product_with_image = Product.objects.create(
                    category=self.category,
                    name='Товар с фото',
                    slug='tovar-s-foto',
                    description='Товар с изображением.',
                    price='1599.00',
                    image=image_content,
                    is_available=True,
                )
                self.assertTrue(product_with_image.image.url.startswith(settings.MEDIA_URL))
                response = self.client.get(reverse('products:detail', kwargs={'slug': product_with_image.slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, settings.MEDIA_URL)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class AdminAccessTests(TestCase):
    def test_admin_site_registration_and_access(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        logged_in = self.client.login(username='admin', password='adminpass')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site administration')
