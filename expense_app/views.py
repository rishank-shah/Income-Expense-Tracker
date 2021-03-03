from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages
from django.utils.timezone import localtime

@login_required(login_url='login')
def dashboard(request):
    return render(request,'expense_app/dashboard.html')

@login_required(login_url='login')
def expense_page(request):
    return render(request,'expense_app/expense.html')

@login_required(login_url='login')
def add_expense(request):
    if Category.objects.filter(user=request.user).exists():
        categories = Category.objects.filter(user=request.user)
        context = {
            'categories' : categories,
            'values':request.POST
    	}
        if request.method == 'GET':
            return render(request,'expense_app/add_expense.html',context)
        if request.method == 'POST':
            amount = request.POST.get('amount',None)
            description = request.POST.get('description','')
            category = request.POST.get('category','')
            date = request.POST.get('expense_date','')
            if amount== None:
                messages.error(request,'Amount cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            amount = int(amount)
            if amount <= 0:
                messages.error(request,'Amount should be greater than zero')
                return render(request,'expense_app/add_expense.html',context)
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            if category == '':
                messages.error(request,'Category cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            if date == '':
                date = localtime()
            category_obj = Category.objects.get(user=request.user,name =category)
            Expense.objects.create(user=request.user,amount=amount,date=date,description=description,category=category_obj).save()
            messages.success(request,'Expense Saved Successfully')
            return redirect('expense')
    else:
        messages.error(request,'Please add a category first.')
        return redirect('add_expense_category')

def add_expense_category(request):
    categories = Category.objects.filter(user=request.user)
    context = {
        'categories' : categories,
        'values':request.POST
    }
    if request.method == 'GET': 
        return render(request,'expense_app/add_expense_category.html',context)
    if request.method == 'POST':
        name = request.POST.get('name','')
        if name == '':
            messages.error(request,'Category cannot be empty')
            return render(request,'expense_app/add_expense_category.html',context)
        Category.objects.create(user=request.user,name = name).save()
        messages.success(request,'Category added')
        return render(request,'expense_app/add_expense_category.html')