from django.test import TestCase

from .models import Product


class ProductTests(TestCase):
    def test_product_string_representation(self):
        product = Product.objects.create(name="Кава", price="125.00")
        self.assertEqual(str(product), "Кава")

# Create your tests here.
