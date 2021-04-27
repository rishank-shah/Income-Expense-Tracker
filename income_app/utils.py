from .models import Income
from django.utils import timezone
from datetime import timedelta
from auth_app.utils import EmailThread
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from user_profile.models import UserProfile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def queryset_filter(user,filter_by):
    today_date_time = timezone.localtime()
    if filter_by.lower() == 'today':
        incomes = Income.objects.filter(user=user,date = today_date_time.date())

    elif filter_by.lower() == 'week':
        week_date_time = today_date_time - timedelta(days=7)
        incomes = Income.objects.filter(user=user,date__gte=week_date_time.date())
    
    elif filter_by.lower() == 'month':
        incomes = Income.objects.filter(user=user,date__year=today_date_time.year,date__month=today_date_time.month)
    
    else:
        incomes = Income.objects.filter(user=user,date__year=today_date_time.year)
    
    return incomes


def income_send_success_mail(request,filename,number_of_incomes,type):	
    if UserProfile.objects.get(user=request.user).email_preference:	
        domain = get_current_site(request).domain
        login_url = 'https://' + domain + '/auth/login/'
        email_subject = f'Incomes Loaded From {type} File'
        email_body = f'Incomes from your {type} file {filename} are successfully loaded. Total Number of incomes loaded are {number_of_incomes}. \n Press the button below to login into your account.'
        extra_info = "You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain
        fromEmail = 'noreply@income-expense.com'
        html_content = render_to_string("partials/_email_template.html",{
            'email_html_title':email_subject,
            'email_title':f'Hi {request.user.username}',
            'email_body':email_body,
            'button_text':'Login',
            'extra_info':extra_info,
            'btn_url':login_url,
            'help_text':"If that doesn't work, copy and paste the following link in your browser:",
            'import_success':True
        })
        text_content = strip_tags(html_content)
        EmailThread(email_subject, text_content, fromEmail,request.user.email,html_content).start()


def income_send_error_mail(request,filename,type):		
    if UserProfile.objects.get(user=request.user).email_preference:
        domain = get_current_site(request).domain
        login_url = 'https://' + domain + '/auth/login/'
        email_subject = f'Income cannot be Loaded From {type} File'
        email_body = f'Income from your {type} file {filename} are not loaded. Please check if the format of the {type} file was as mentioned. \n'
        extra_info = "You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain
        fromEmail = 'noreply@income-expense.com'
        html_content = render_to_string("partials/_email_template.html",{
            'email_html_title':email_subject,
            'email_title':f'Hi {request.user.username}',
            'email_body':email_body,
            'button_text':'Login',
            'extra_info':extra_info,
            'btn_url':login_url,
            'help_text':"If that doesn't work, copy and paste the following link in your browser:",
            'import_fail':True
        })
        text_content = strip_tags(html_content)
        EmailThread(email_subject, text_content, fromEmail,request.user.email,html_content).start()