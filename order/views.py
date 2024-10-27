from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import CartItem, Order
from main.models import Makanan
from django.contrib.auth.models import User
from order.forms import CartItemForm
from django.contrib.auth.decorators import login_required

@login_required
def show_cart(request):
    user = request.user
    try:
        order = Order.objects.get(user=user, is_checked_out=False)
        cart_items = order.cart_items.all()
        total = order.total()
    except Order.DoesNotExist:
        cart_items = None
        total = 0

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'order/cart.html', context)

@login_required
def show_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, is_checked_out=True)
    cart_items = order.cart_items.all()
    total = order.total()

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'order/order_confirmation.html', context)

@login_required
def create_order(request, product_id):
    user = request.user
    product = get_object_or_404(Makanan, pk=product_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, initial={'product': product, 'quantity': 1})
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = user
            cart_item.save()

            messages.success(request, f'Product "{product.food_name}" has been added to your cart.')
            order, created = Order.objects.get_or_create(user=user, is_checked_out=False)
            order.cart_items.add(cart_item)
            order.save()

            return redirect('main:show_main')
    else:
        form = CartItemForm(initial={'product': product})
    return render(request, 'order/add_to_cart.html', {'form': form})

@login_required
def checkout(request):
    user = request.user  
    order = Order.objects.filter(user=user, is_checked_out=False).first()
    if not order:
        return HttpResponse("Your cart is empty.", status=404)

    if request.method == 'POST':
        order.is_checked_out = True
        order.save()
        return redirect('order:order_confirmation', order_id=order.id)

    cart_items = order.cart_items.all()
    total = order.total()
    return render(request, 'order/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, is_checked_out=True)
    return render(request, 'order/order_confirmation.html', {'order': order})

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('order:cart_view')
        else:
            return render(request, 'order/edit_cart_item.html', {'form': form, 'item_id': item_id})
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'order/edit_cart_item.html', {'form': form, 'item_id': item_id})

@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('order:cart_view')
    return HttpResponse("This endpoint requires a POST request.", status=405)
'''
@login_required
def show_cart(request):
    user = request.user
    try:
        order = Order.objects.get(user=user, is_checked_out=False)
        cart_items = order.cart_items.all()
        total = order.total()
    except Order.DoesNotExist:
        cart_items = None
        total = 0

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'order/cart.html', context)

@login_required
def show_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, is_checked_out=True)
    cart_items = order.cart_items.all()
    total = order.total()

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'order/order_confirmation.html', context)


def create_order(request, product_id):
    user = request.user
    product = get_object_or_404(Makanan, pk=product_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, initial={'product': product, 'quantity': 1})
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = user
            cart_item.save()

            messages.success(request, f'Product "{product.food_name}" has been added to your cart.')
            order, created = Order.objects.get_or_create(user=user, is_checked_out=False)
            order.cart_items.add(cart_item)
            order.save()

            return redirect('main:show_main')
    else:
        form = CartItemForm(initial={'product': product})
    return render(request, 'order/add_to_cart.html', {'form': form})

def checkout(request):
    user = request.user  
    order = Order.objects.filter(user=user, is_checked_out=False).first()
    if not order:
        return HttpResponse("Your cart is empty.", status=404)

    if request.method == 'POST':
        order.is_checked_out = True
        order.save()
        return redirect('order:order_confirmation', order_id=order.id)

    cart_items = order.cart_items.all()
    total = order.total()
    return render(request, 'order/checkout.html', {'cart_items': cart_items, 'total': total})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, is_checked_out=True)
    return render(request, 'order/order_confirmation.html', {'order': order})


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('order:cart_view')
        else:
            return render(request, 'order/edit_cart_item.html', {'form': form, 'item_id': item_id})
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'order/edit_cart_item.html', {'form': form, 'item_id': item_id})

def delete_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('order:cart_view')
    return HttpResponse("This endpoint requires a POST request.", status=405)'''