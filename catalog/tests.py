from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders

from .models import Product


class ProductTests(TestCase):
    def test_catalog_urls_are_reversed_by_names(self):
        self.assertEqual(reverse("catalog:product_list"), "/products/")
        self.assertEqual(reverse("catalog:product_create"), "/products/new/")

    def test_product_string_representation(self):
        product = Product.objects.create(name="Кава", price="125.00")
        self.assertEqual(str(product), "Кава")

    def test_products_page_uses_empty_state(self):
        response = self.client.get("/products/")
        self.assertContains(response, "Товарів немає.")

    def test_catalog_stylesheet_is_discoverable_and_loaded(self):
        response = self.client.get("/products/")
        self.assertIsNotNone(finders.find("catalog/css/style.css"))
        self.assertContains(response, '/static/catalog/css/style.css')

    def test_custom_filter_and_tag_render_product_data(self):
        Product.objects.create(name="Кава", price="125.50", quantity=3)
        Product.objects.create(name="Чай", price="80.00", quantity=2)

        response = self.client.get("/products/")

        self.assertContains(response, "125.50 грн")
        self.assertContains(response, "Товарів у базі: 2")
        self.assertContains(response, "2 товари")

    def test_product_name_is_autoescaped(self):
        Product.objects.create(name="<script>alert(1)</script>", price="10.00")
        response = self.client.get("/products/")
        self.assertNotContains(response, "<script>alert(1)</script>", html=False)
        self.assertContains(response, "&lt;script&gt;", html=False)

    def test_create_product_uses_post_redirect_get_and_message(self):
        response = self.client.post(
            "/products/new/",
            {
                "name": "Кава",
                "description": "Зернова",
                "price": "125.50",
                "quantity": "4",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/products/")
        self.assertEqual(Product.objects.get().name, "Кава")
        response = self.client.get("/products/")
        self.assertContains(response, "Товар успішно додано.")
        response = self.client.get("/products/")
        self.assertNotContains(response, "Товар успішно додано.")

# Create your tests here.
