from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create_order/<uuid:product_id>/', views.create_order, name='create_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/', views.show_cart, name='show_cart'),
    path('order/<int:order_id>/', views.show_order, name='show_order'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('show_order/', views.show_order, name='show_order'),
]
