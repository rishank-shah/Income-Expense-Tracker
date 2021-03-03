from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    return render(request,'expense_app/dashboard.html')

@login_required(login_url='login')
def expense_page(request):
    return render(request,'expense_app/expense.html')

@login_required(login_url='login')
def add_expense(request):
    return render(request,'expense_app/add_expense.html')