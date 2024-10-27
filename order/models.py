from django.db import models
from django.conf import settings
from main.models import Makanan  # Mengimport model Makanan dari aplikasi 'main'

from django.core.exceptions import ValidationError

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Makanan, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def clean(self):
        # Example validation: Ensure the user is marked as a buyer
        if not hasattr(self.user, 'is_buyer') or not self.user.is_buyer:
            raise ValidationError("Only buyers can add items to the cart.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    order_date = models.DateField(auto_now_add=True)
    is_checked_out = models.BooleanField(default=False)

    def clean(self):
        # Example validation: Check something specific about the order or user
        if not self.user.is_active:
            raise ValidationError("Only active users can create orders.")
    
    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
