from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url = 'login')
def profile(request):
    if request.method == 'GET':
        user_profile = UserProfile.objects.filter(user=request.user)
        if user_profile.exists():
            user_profile_obj = UserProfile.objects.get(user=request.user)
            return render(request,'user_app/profile.html',user_profile_obj)
        else:
            return render(request,'user_app/profile.html')