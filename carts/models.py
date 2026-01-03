from django.db import models

# Create your models here.
from products.models import Product, Variation
# To solve the error: "Cannot convert float to Decimal.  First convert the float to a string"
# The Decimal field "0.00" need to be replaced by "Decimal(str(0.00))"
from decimal import Decimal

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)
    line_total = models.DecimalField(default=Decimal(10.99), max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
       try:
           return str(self.cart.id)
       except:
           return self.product.title


class Cart(models.Model):
    #items = models.ManyToManyField(CartItem, blank=True)
    #products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal(0.00))
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id: %s" % (self.id)
