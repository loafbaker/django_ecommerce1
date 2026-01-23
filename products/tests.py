from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductImage


class ProductViewTests(TestCase):
    def test_single_product_missing_slug_returns_404(self):
        url = reverse('single_product', kwargs={'slug': 'missing-slug'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_single_product_renders_template_with_images(self):
        product = Product.objects.create(title='Test Product', slug='test-product')
        image = ProductImage.objects.create(
            product=product,
            image='products/images/test.jpg',
        )
        url = reverse('single_product', kwargs={'slug': product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/single.html')
        self.assertEqual(response.context['product'], product)
        self.assertIn(image, response.context['images'])
