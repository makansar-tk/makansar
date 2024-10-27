from django.db import models
from django.conf import settings
from django.forms import ValidationError
from main.models import Makanan  # Mengimport model Makanan dari aplikasi 'main'
from account.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def clean(self):
        super().clean()
        if not self.user.buyer:
            raise ValidationError("Hanya pengguna dengan akses buyer yang diizinkan.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is called
        super().save(*args, **kwargs)
    product = models.ForeignKey(Makanan, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def clean(self):
        super().clean()
        if not self.user.buyer:
            raise ValidationError("Hanya pengguna dengan akses buyer yang diizinkan.")

    def save(self, args, **kwargs):
        self.clean()
        super().save(args, **kwargs)
    cart_items = models.ManyToManyField(CartItem)
    order_date = models.DateField(auto_now_add=True)
    is_checked_out = models.BooleanField(default=False)  

    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
