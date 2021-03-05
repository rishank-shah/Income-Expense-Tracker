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
    #TODO: create a updated_at in income and expense and also display according to that in recent activity
    today_date_time = timezone.localtime()
    start = today_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end = today_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    incomes = Income.objects.filter(user=request.user,created_at__range=(start,end)).order_by('-created_at')
    expenses = Expense.objects.filter(user=request.user,created_at__range=(start,end)).order_by('-created_at')
    spend_today = expenses.aggregate(Sum('amount'))
    return render(request,'dashboard.html',{
        'expenses':expenses,
        'incomes':incomes,
        'spent_today':spend_today['amount__sum']
    })