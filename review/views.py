from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Review
from main.models import Makanan  # Adjust import based on FoodItem model location
from .forms import ReviewForm  # Create this form

# # View to add a review
# @login_required
def add_review(request, food_id):
    food_item = get_object_or_404(Makanan, id=food_id)

    # Check if the user is in the "Pembeli" group
    # if not request.user.groups.filter(name='Pembeli').exists():
    #     return redirect('no_access')  

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.buyer = request.user
            review.food_item = food_item
            review.save()
            return redirect('food_detail', food_id=food_id)
    else:
        form = ReviewForm()

    return render(request, 'review/add_review.html', {'form': form, 'food_item': food_item})

# View to display reviews for a food item
def food_reviews(request, food_id):
    food_item = get_object_or_404(Makanan, id=food_id)
    reviews = Review.objects.filter(food_item=food_item)

    if not request.user.groups.filter(name='Pembeli').exists():
        return redirect('no_access')  
    
    return render(request, 'review/food_reviews.html', {'food_item': food_item, 'reviews': reviews})
