from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expense_app.models import Expense
from income_app.models import Income
from itertools import chain
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

@login_required(login_url='login')
def dashboard(request):
    today_date_time = timezone.localtime()
    week_date_time = today_date_time - timedelta(days=7) 
    start_today_data = today_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today_data = today_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    incomes_today = Income.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')
    expenses_today = Expense.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')
    expenses_month = Expense.objects.filter(user=request.user,created_at__year=today_date_time.year,created_at__month=today_date_time.month)
    expenses_year = Expense.objects.filter(user=request.user,created_at__year=today_date_time.year)
    expenses_week = Expense.objects.filter(user=request.user,created_at__gte=week_date_time)
    spent_month_count = expenses_month.count()
    spent_year_count = expenses_year.count()
    spent_week_count = expenses_week.count()
    spent_month = expenses_month.aggregate(Sum('amount'))
    spend_today = expenses_today.aggregate(Sum('amount'))
    spent_week = expenses_week.aggregate(Sum('amount'))
    spent_year = expenses_year.aggregate(Sum('amount'))
    return render(request,'dashboard.html',{
        'expenses':expenses_today,
        'incomes':incomes_today,
        'spent_today':spend_today['amount__sum'],
        'spent_month':spent_month['amount__sum'],
        'spent_month_count':spent_month_count,
        'spent_year':spent_year['amount__sum'],
        'spent_year_count':spent_year_count,
        'spent_week':spent_week['amount__sum'],
        'spent_week_count':spent_week_count,
    })