from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import load_currency_data

@login_required(login_url = 'login')
def profile(request):
    currency_data = load_currency_data()
    user = User.objects.get(username = request.user.username)
    if request.method == 'GET':
        user_profile = UserProfile.objects.filter(user=user)
        if user_profile.exists():
            user_profile_obj = UserProfile.objects.get(user=user)
            return render(request,'user_app/profile.html',{'first_name':user.first_name,'last_name':user.last_name,'profile_pic':user_profile_obj.profile_pic,'currency_data':currency_data,'selected_currency':user_profile_obj.currency})
        else:
            return render(request,'user_app/profile.html',{'first_name':user.first_name,'last_name':user.last_name,'currency_data':currency_data,'selected_currency':'INR - Indian Rupee'})

    if request.method == 'POST':
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        if first_name == '' or last_name == '':
            messages.error(request,'First and Last Name cannot be empty')
            return redirect('user_profile')
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfile.objects.filter(user=request.user)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if user_profile.exists():
            user_profile_obj = UserProfile.objects.get(user=user)
            user_profile_obj.profile_pic = request.FILES.get('profile_pic',user_profile_obj.profile_pic)
            user_profile_obj.save()
            messages.success(request,'Profile Updated Succesfully')
        else:
            user_profile_obj = UserProfile.objects.create(user=user,profile_pic = request.FILES.get('profile_pic'))
            user_profile_obj.save()
            messages.success(request,'Profile Created Succesfully')
        return render(request,'user_app/profile.html',{'first_name':user.first_name,'last_name':user.last_name,'profile_pic':user_profile_obj.profile_pic,'currency_data':currency_data,'selected_currency':user_profile_obj.currency})

@login_required(login_url = 'login')
def save_currency(request):
    user = User.objects.get(username = request.user.username)
    user_profile = UserProfile.objects.filter(user=user).exists()
    user_profile_obj = None
    if user_profile:
        user_profile_obj = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        currency = request.POST.get('currency')
        if user_profile:
            user_profile_obj.currency = currency
            user_profile_obj.save()
        else:
            UserProfile.objects.create(user = request.user,currency = currency )
        messages.success(request,"Currency saved")
        return redirect('user_profile')
    else:
        return redirect('user_profile')