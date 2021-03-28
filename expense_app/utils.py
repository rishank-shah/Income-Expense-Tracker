from expense_app.models import Expense
from django.utils import timezone
from datetime import timedelta
from auth_app.utils import EmailThread
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

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

def expense_send_success_mail(request,filename,number_of_expenses):		
    domain = get_current_site(request).domain
    email_subject = 'Expenses Loaded From Csv File'
    email_body = f'Hi {request.user.username}. Expenses from your csv file {filename} are successfully loaded. Total Number of expenses loaded are {number_of_expenses} \n'
    fromEmail = 'noreply@income-expense.com'
    email = EmailMessage(
        email_subject,
        email_body,
        fromEmail,
        [request.user.email],
    )
    EmailThread(email).start()

def expense_send_error_mail(request,filename):		
    domain = get_current_site(request).domain
    email_subject = 'Expenses cannot be Loaded From Csv File'
    email_body = f'Hi {request.user.username}. Expenses from your csv file {filename} are not loaded. Please check if the format of the csv file was as mentioned. \n'
    fromEmail = 'noreply@income-expense.com'
    email = EmailMessage(
        email_subject,
        email_body,
        fromEmail,
        [request.user.email],
    )
    EmailThread(email).start()