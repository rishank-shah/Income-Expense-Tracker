from django.shortcuts import render
from django.views import View

class Registration(View):
    def get(self,request):
        return render(request,'auth_app/register.html')
    def post(self,request):
        pass

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