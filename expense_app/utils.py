from expense_app.models import Expense
from django.utils import timezone
from datetime import timedelta

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