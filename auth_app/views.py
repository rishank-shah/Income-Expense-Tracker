from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
class Registration(View):
    def get(self,request):
        return render(request,'auth_app/register.html')
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        context = {
            "values": request.POST
        }

        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages(request,'Password is too short')
                return render(request,'auth_app/register.html',context=context)
            
            user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
            user.set_password(password)
            user.is_active = False
            user.save()



class Login(View):
    def get(self,request):
        return render(request,'auth_app/login.html')
    def post(self,request):
        pass

class Logout(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')