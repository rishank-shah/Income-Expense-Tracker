from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, ExpenseCategory
from django.contrib import messages
from django.utils.timezone import localtime
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum
import xlwt
from .utils import queryset_filter
import csv

@login_required(login_url='login')
def expense_page(request):
    expenses =  Expense.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(expenses,4)
    page_number = request.GET.get('page')
    page_expenses = Paginator.get_page(paginator,page_number)
    if UserProfile.objects.filter(user = request.user).exists():
        currency = UserProfile.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'
    return render(request,'expense_app/expense.html',{
        'currency':currency,
        'page_expenses':page_expenses,
        'expenses':expenses
    })

@login_required(login_url='login')
def add_expense(request):
    if ExpenseCategory.objects.filter(user=request.user).exists():
        categories = ExpenseCategory.objects.filter(user=request.user)
        context = {
            'categories' : categories,
            'values':request.POST
        }
        if request.method == 'GET':
            return render(request,'expense_app/add_expense.html',context)
        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            category = request.POST.get('category','')
            date = request.POST.get('expense_date','')
            if amount== '':
                messages.error(request,'Amount cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            amount = float(amount)
            if amount <= 0:
                messages.error(request,'Amount should be greater than zero')
                return render(request,'expense_app/add_expense.html',context)
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            if category == '':
                messages.error(request,'ExpenseCategory cannot be empty')
                return render(request,'expense_app/add_expense.html',context)
            if date == '':
                date = localtime()
            category_obj = ExpenseCategory.objects.get(user=request.user,name =category)
            Expense.objects.create(
                user=request.user,
                amount=amount,
                date=date,
                description=description,
                category=category_obj
            ).save()
            messages.success(request,'Expense Saved Successfully')
            return redirect('expense')
    else:
        messages.error(request,'Please add a category first.')
        return redirect('add_expense_category')

@login_required(login_url='login')
def add_expense_category(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    context = {
        'categories' : categories,
        'values':request.POST
    }
    if request.method == 'GET': 
        return render(request,'expense_app/add_expense_category.html',context)
    if request.method == 'POST':
        name = request.POST.get('name','')
        if name == '':
            messages.error(request,'Expense Category cannot be empty')
            return render(request,'expense_app/add_expense_category.html',context)
        name = name.lower().capitalize()
        if ExpenseCategory.objects.filter(user=request.user,name = name).exists():
            messages.error(request,f'Expense Category ({name}) already exists.')
            return render(request,'expense_app/add_expense_category.html',context)
        ExpenseCategory.objects.create(user=request.user,name = name).save()
        messages.success(request,'Expense Category added')
        return render(request,'expense_app/add_expense_category.html',{
            'categories' : categories,
        })

@login_required(login_url='login')
def delete_expense_category(request,id):
    if ExpenseCategory.objects.filter(id=id).exists():
        category = ExpenseCategory.objects.get(id=id)
        user = User.objects.get(username=request.user.username)
        if category.user != user:
            messages.error(request,'You cannot delete this catgeory.')
            return redirect('add_expense_category')
        else:
            category.delete()
            messages.success(request,'Deleted category')
            return redirect('add_expense_category')
    messages.error(request,'Please try again')
    return redirect('add_expense_category')

@login_required(login_url='login')
def edit_expense(request,id):
    categories = ExpenseCategory.objects.filter(user=request.user)
    if Expense.objects.filter(id=id,user=request.user).exists():
        expense = Expense.objects.get(id=id,user=request.user)
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense')
    context = {
        'expense':expense,
        'values': expense,
        'categories':categories
    }
    if request.method == 'GET':
        return render(request,'expense_app/edit_expense.html',context)

    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        category = request.POST.get('category','')
        date = request.POST.get('expense_date','')
        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'expense_app/edit_expense.html',context)
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'expense_app/edit_expense.html',context)
        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'expense_app/edit_expense.html',context)
        if category == '':
            messages.error(request,'ExpenseCategory cannot be empty')
            return render(request,'expense_app/edit_expense.html',context)
        if date == '':
            date = localtime()
        category_obj = ExpenseCategory.objects.get(user=request.user,name =category)
        expense.amount = amount
        expense.date = date
        expense.category = category_obj
        expense.description = description
        expense.save() 
        messages.success(request,'Expense Updated Successfully')
        return redirect('expense')

@login_required(login_url='login')
def delete_expense(request,id):
    if Expense.objects.filter(id=id,user=request.user).exists():
        Expense.objects.get(id=id,user=request.user).delete()
        messages.success(request,'Expense Deleted Successfully')
        return redirect('expense')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense')

@login_required(login_url='login')
def download_as_excel(request,filter_by):
    filter_by = str(filter_by)
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses-'+ str(request.user.username) + str(localtime())+".xls"
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    if filter_by != '':
        ws.write(0,0,f"Expenses in {filter_by.lower().capitalize()}")
    else:
        ws.write(0,0,f"Expenses in Year")
    row_number = 1
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True
    columns = ['Date','Category','Description','Amount']
    for col_num in range(len(columns)):
        ws.write(row_number,col_num,columns[col_num],fontStyle)
    fontStyle = xlwt.XFStyle()
    expenses = queryset_filter(User.objects.get(username=request.user.username),filter_by).order_by('date')
    rows = expenses.values_list('date','category__name','description','amount')
    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            ws.write(row_number,col_num,str(row[col_num]),fontStyle)
    row_number +=2
    style = xlwt.easyxf('font: colour red, bold True;')
    ws.write(row_number,0,'TOTAL',style)
    ws.write(row_number,3,str(expenses.aggregate(Sum('amount'))['amount__sum']),style)
    wb.save(response)
    return response

@login_required(login_url='login')
def download_as_csv(request,filter_by):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(request.user.username) + str(localtime()) + ".csv"
    writer = csv.writer(response)
    writer.writerow(['Date','Category','Description','Amount'])
    expenses = queryset_filter(User.objects.get(username=request.user.username),filter_by).order_by('date')
    for expense in expenses:
        writer.writerow([expense.date,expense.category.name,expense.description,expense.amount])
    writer.writerow(['','','',''])
    writer.writerow(['TOTAL','','',str(expenses.aggregate(Sum('amount'))['amount__sum'])])
    return response