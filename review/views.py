from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Makanan
from .forms import ReviewForm
from django.http import JsonResponse


def show_reviews(request, makanan_id):
    makanan = get_object_or_404(Makanan, id=makanan_id)
    reviews = makanan.review_set.all()
    return render(request, 'show_reviews.html', {'makanan': makanan, 'reviews': reviews})

@login_required
def tambah_review(request, makanan_id):
    makanan = get_object_or_404(Makanan, id=makanan_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.buyer = request.user
            review.food_item = makanan
            review.save()

            # Update jumlah review dan rating
            makanan.jumlah_review += 1
            total_rating = sum(r.rating for r in makanan.review_set.all()) + makanan.rating_default  # Tambahkan rating default
            makanan.new_rating = total_rating / (makanan.jumlah_review + 1)  # Bagi dengan jumlah review + 1
            makanan.save()

            return redirect('review:show_reviews', makanan_id=makanan.id)
    else:
        form = ReviewForm()
    return render(request, 'tambah_review.html', {'form': form, 'makanan': makanan})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, buyer=request.user)
    makanan = review.food_item
    original_rating = review.rating

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.buyer = request.user
            updated_review.food_item = makanan
            updated_review.save()

            # Update rating dengan mempertimbangkan rating default
            total_rating = sum(r.rating for r in makanan.review_set.all()) + makanan.rating_default
            makanan.new_rating = total_rating / (makanan.jumlah_review + 1)
            makanan.save()

            return redirect('review:show_reviews', makanan_id=makanan.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def hapus_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, buyer=request.user)
    makanan = review.food_item

    # Update jumlah review dan rating setelah penghapusan
    makanan.jumlah_review -= 1
    review.delete()

    if makanan.jumlah_review > 0:
        total_rating = sum(r.rating for r in makanan.review_set.all()) + makanan.rating_default
        makanan.new_rating = total_rating / (makanan.jumlah_review + 1)
    else:
        makanan.new_rating = makanan.rating_default  # Kembali ke rating default jika tidak ada review

    makanan.save()
    return redirect('review:show_reviews', makanan_id=makanan.id)
