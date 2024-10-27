from django.db import models
from django.conf import settings
from main.models import Makanan  # Mengimport model Makanan dari aplikasi 'main'

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Makanan, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    order_date = models.DateField(auto_now_add=True)
    is_checked_out = models.BooleanField(default=False)  

    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
