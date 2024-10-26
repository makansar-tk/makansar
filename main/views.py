from django.shortcuts import render, redirect
from main.models import Makanan, UserProfile
from account.models import User
from main.forms import ProductEntryForm, UserForm, UserProfileForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required(login_url='/login')
def show_main(request):
    product_entries = Makanan.objects.all()

    context = {
        'team' : 'D04',
        'product_entries' : product_entries,
    }

    return render(request, "buyer.html", context)

def create_product_entry(request):
    form = ProductEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product_entry.html", context)

def logout_user(request):
    logout(request)
    return redirect('account:login')

# Fungsi view user profile
def view_profile(request):
    return render(request, 'profile.html')

# Fungsi edit dashboard (profil user)
def edit_dashboard(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user_profile=user)  # Link with the correct UserProfile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        action = request.POST.get('action')

        if action == 'save' and user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('main:show_main')

        elif action == 'delete':
            return render(request, 'confirm_delete.html')  # Render the confirmation template

        elif action == 'confirm_delete':
            user.delete()
            logout(request)
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('account:login')

        elif action == 'cancel_delete':
            return redirect('main:edit_dashboard')

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'dashboard.html', context)

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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