from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .utils import email_register,account_activation_token
from user_profile.models import UserProfile

class Registration(View):

    def get(self,request):
        return render(request,'auth_app/register.html')

    def post(self,request):
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')

        context = {
            "username":username,
            "email":email,
            "last_name":last_name,
            "first_name":first_name,
        }

        list_context = list(context.values())
        if '' in list_context:
            messages.error(request,"All Fields are required")
            return render(request,'auth_app/register.html',context=context)

        if not User.objects.filter(username=username).exists():
            if  not User.objects.filter(email=email).exists():
                if password != password2:
                    messages.error(request,"Passwords don't match")
                    return render(request,'auth_app/register.html',context=context)
                if len(password) < 6:
                    messages.error(request,'Password is too short')
                    return render(request,'auth_app/register.html',context=context)
                
                user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.is_active = False
                user.save()
                UserProfile.objects.create(user=user).save()
                email_register(request,user,email)
                messages.success(request,'Account Created Succesfully. Please Confirm Email')
                return redirect('login')
            else:
                messages.error(request,'Email Already exists')
                return render(request,'auth_app/register.html',context=context)
        else:
            messages.error(request,'Username Already exists')
            return render(request,'auth_app/register.html',context=context)

class Login(View):

    def get(self,request):
        return render(request,'auth_app/login.html')

    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'auth_app/login.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'auth_app/login.html',context=context)

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if not user.is_active:
                    messages.error(request,'Please Activate Account.')
                    return render(request,'auth_app/login.html')
                elif user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")
                    return redirect('dashboard')
            else:
                messages.error(request,'Invalid credentials')
                return render(request,'auth_app/login.html',context=context)
        else:
            messages.error(request,'Something went wrong.')
            return render(request,'auth_app/login.html',context=context)



class Logout(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')


class Verification(View):

	def get(self,request,uidb64,token):
        
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)

			if not account_activation_token.check_token(user,token):
				messages.error(request,'Already Activated')
				return redirect('login')

			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('login')