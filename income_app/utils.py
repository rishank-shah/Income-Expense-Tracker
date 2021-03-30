from .models import Income
from django.utils import timezone
from datetime import timedelta
from auth_app.utils import EmailThread
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from user_profile.models import UserProfile

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

def income_send_success_mail(request,filename,number_of_incomes):	
    if UserProfile.objects.get(user=request.user).email_preference:	
        domain = get_current_site(request).domain
        email_subject = 'Incomes Loaded From Csv File'
        email_body = f'Hi {request.user.username}. Incomes from your csv file {filename} are successfully loaded. Total Number of incomes loaded are {number_of_incomes} \n'
        fromEmail = 'noreply@income-expense.com'
        email = EmailMessage(
            email_subject,
            email_body,
            fromEmail,
            [request.user.email],
        )
        EmailThread(email).start()

def income_send_error_mail(request,filename):		
    if UserProfile.objects.get(user=request.user).email_preference:
        domain = get_current_site(request).domain
        email_subject = 'Income cannot be Loaded From Csv File'
        email_body = f'Hi {request.user.username}. Income from your csv file {filename} are not loaded. Please check if the format of the csv file was as mentioned. \n'
        fromEmail = 'noreply@income-expense.com'
        email = EmailMessage(
            email_subject,
            email_body,
            fromEmail,
            [request.user.email],
        )
        EmailThread(email).start()