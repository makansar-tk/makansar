from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CartItem, Order
from main.models import Makanan
from .forms import CartItemForm

User = get_user_model()

class OrderTestCase(TestCase):
    def test_views(self):
        # Ensure the cart view works for logged in user
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/order/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nasi Goreng Kambing')

        # Test redirection for anonymous user
        self.client.logout()
        response = self.client.get('/order/cart/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/order/cart/') 

    def test_cart_item_creation(self):
        # Test CartItem Creation
        cart_item = CartItem.objects.create(user=self.user, product=self.makanan, quantity=3)
        self.assertEqual(cart_item.subtotal, 105000)  # 35000 * 3

    def test_order_total(self):
        # Test order total calculation
        order = Order.objects.create(user=self.user)
        cart_item = CartItem.objects.create(user=self.user, product=self.makanan, quantity=2)
        order.cart_items.add(cart_item)
        self.assertEqual(order.total(), 70000)  # 35000 * 2

    def test_cart_item_form(self):
        # Test the form is valid and saves correctly
        form_data = {'quantity': 2, 'product': self.makanan.id}
        form = CartItemForm(data=form_data)
        self.assertTrue(form.is_valid())
        cart_item = form.save(commit=False)
        cart_item.user = self.user
        cart_item.save()
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(cart_item.quantity, 2)

     # adjust the redirect URL based on your login route

# More detailed view tests can be added here, testing the behavior of each view
