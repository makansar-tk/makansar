from django.shortcuts import render, redirect
from main.models import Makanan, UserProfile
from main.forms import ProductEntryForm, UserProfileForm
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from review.models import Review

# Create your views here.

def show_main(request):
    product_entries = Makanan.objects.all()
    kategori_list = Makanan.objects.values_list('category', flat=True).distinct()
    context = {
        'team' : 'D04',
        'product_entries' : product_entries,
        'kategori_list': kategori_list,
    }

    return render(request, "buyer.html", context)

def create_product_entry(request):
    form = ProductEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product_entry.html", context)

# Fungsi dashboard
def edit_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(id=1)  # Sementara pakai ini saat belum ada login form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        action = request.POST.get('action')

        if action == 'save' and form.is_valid():
            form.save()
            return redirect('main:show_main')

        elif action == 'delete':
            form = UserProfileForm()
            return render(request, 'dashboard.html', {'form': form})

    else:
        form = UserProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'dashboard.html', context)

def show_xml(request):
    data = Makanan.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id):
    data = Makanan.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Makanan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Makanan.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_makanan_by_kategori(request):
    kategori = request.GET.get('kategori')
    makanan_list = Makanan.objects.filter(category=kategori)
    data = [{
        'id': makanan.id,
        'food_name': makanan.food_name,
        'price': float(makanan.price),
        'rating_default': float(makanan.rating_default),
        'image': makanan.image.url if makanan.image else None
    } for makanan in makanan_list]
    return JsonResponse(data, safe=False)

def get_makanan_detail(request):
    makanan_id = request.GET.get('id')
    makanan = Makanan.objects.get(id=makanan_id)
    data = {
        'id': makanan.id,
        'food_name': makanan.food_name,
        'description': makanan.food_desc,
        'price': makanan.price,
        'image': makanan.image.url if makanan.image else '/static/images/default-food.jpeg',
        'rating_default': makanan.rating_default,
    }
    return JsonResponse(data)