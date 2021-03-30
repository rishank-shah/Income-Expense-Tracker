from expense_app.models import Expense
from django.utils import timezone
from datetime import timedelta
from auth_app.utils import EmailThread
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from user_profile.models import UserProfile

def queryset_filter(user,filter_by):
    today_date_time = timezone.localtime()
    if filter_by.lower() == 'today':
        expenses = Expense.objects.filter(user=user,date = today_date_time.date())

    elif filter_by.lower() == 'week':
        week_date_time = today_date_time - timedelta(days=7)
        expenses = Expense.objects.filter(user=user,date__gte=week_date_time.date())

    elif filter_by.lower() == 'month':
        expenses = Expense.objects.filter(user=user,date__year=today_date_time.year,date__month=today_date_time.month)

    else:
        expenses = Expense.objects.filter(user=user,date__year=today_date_time.year)
        
    return expenses

def expense_send_success_mail(request,filename,number_of_expenses,type):
    if UserProfile.objects.get(user=request.user).email_preference:
        domain = get_current_site(request).domain
        email_subject = f'Expenses Loaded From {type} File'
        email_body = f'Hi {request.user.username}. Expenses from your {type} file {filename} are successfully loaded. Total Number of expenses loaded are {number_of_expenses} \n'
        fromEmail = 'noreply@income-expense.com'
        email = EmailMessage(
            email_subject,
            email_body,
            fromEmail,
            [request.user.email],
        )
        EmailThread(email).start()

def expense_send_error_mail(request,filename,type):	
    if UserProfile.objects.get(user=request.user).email_preference:	
        domain = get_current_site(request).domain
        email_subject = f'Expenses cannot be Loaded From {type} File'
        email_body = f'Hi {request.user.username}. Expenses from your {type} file {filename} are not loaded. Please check if the format of the {type} file was as mentioned. \n'
        fromEmail = 'noreply@income-expense.com'
        email = EmailMessage(
            email_subject,
            email_body,
            fromEmail,
            [request.user.email],
        )
        EmailThread(email).start()