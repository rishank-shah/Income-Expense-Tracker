from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
from django.http import JsonResponse
from .models import Expense, ExpenseCategory

@login_required(login_url='login')
def expense_summary(request):
    today_date = datetime.date.today()
    filter_by = request.GET.get('filter', None)
    if filter_by != None:
        if filter_by.lower() == 'week':
            date_search =  today_date - timedelta(days=7) 
            expenses = Expense.objects.filter(user=request.user,date__gte=date_search)
            title = 'Expenses per category in this week'
        elif filter_by.lower() == 'month':
            expenses = Expense.objects.filter(user=request.user,date__year=today_date.year,date__month=today_date.month)
            title = 'Expenses per category in this month'
        elif filter_by.lower() == 'year':
            expenses = Expense.objects.filter(user=request.user,date__year=today_date.year)
            title = 'Expenses per category in this year'
        elif filter_by.lower() == 'today':
            expenses = Expense.objects.filter(user=request.user,date__exact=today_date)
            title = 'Expenses per category spent today'
        else:
            six_months_ago = today_date - datetime.timedelta(days = 30*6)
            expenses = Expense.objects.filter(user = request.user,date__gte=six_months_ago)
            title = 'Expenses per category in last six months'
    else:
        six_months_ago = today_date - datetime.timedelta(days = 30*6)
        expenses = Expense.objects.filter(user = request.user,date__gte=six_months_ago)
        title = 'Expenses per category in last six months'
    final_rep = {}
    def get_category(expense):
        return expense.category.name
    category_list = list(set(map(get_category,expenses)))
    def get_expense_category_amount(category):
        amount = 0
        category = ExpenseCategory.objects.get(name=category)
        filtered_by_category = expenses.filter(category=category.id)
        for i in filtered_by_category:
            amount += i.amount
        return amount
    for x in expenses:
        for y in category_list :
            final_rep[y] = get_expense_category_amount(y)
    return JsonResponse({
        'expense_category_data':final_rep,
        'label_title':title
    },safe=False)