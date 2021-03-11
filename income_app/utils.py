from .models import Income
from django.utils import timezone
from datetime import timedelta

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