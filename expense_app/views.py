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
import pandas as pd
import datetime
from .utils import expense_send_success_mail,expense_send_error_mail
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from datetime import datetime as datetime_custom
from django.db.models import Q

@login_required(login_url='login')
def expense_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    expenses =  Expense.objects.filter(
        user = request.user
    ).order_by('-date')

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                expenses = expenses.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                expenses = expenses.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            expenses = expenses.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('expense')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_expenses = Paginator.get_page(paginator,page_number)

    if UserProfile.objects.filter(user = request.user).exists():
        currency = UserProfile.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'

    return render(request,'expense_app/expense.html',{
        'currency':currency,
        'page_expenses':page_expenses,
        'expenses':expenses,
        'filter_context':filter_context,
        'base_url':base_url
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
        'values':request.POST,
        'create':True
    }

    if request.method == 'GET': 
        return render(request,'expense_app/expense_category_import.html',context)

    if request.method == 'POST':
        name = request.POST.get('name','')

        if name == '':
            messages.error(request,'Expense Category cannot be empty')
            return render(request,'expense_app/expense_category_import.html',context)
        
        name = name.lower().capitalize()
        if ExpenseCategory.objects.filter(user=request.user,name = name).exists():
            messages.error(request,f'Expense Category ({name}) already exists.')
            return render(request,'expense_app/expense_category_import.html',context)
        
        ExpenseCategory.objects.create(user=request.user,name = name).save()

        messages.success(request,'Expense Category added')
        return render(request,'expense_app/expense_category_import.html',{
            'categories' : categories,
            'create':True
        })

@login_required(login_url='login')
def edit_expense_category(request,id):

    if ExpenseCategory.objects.filter(user=request.user,pk=id).exists():
        category = ExpenseCategory.objects.get(user=request.user,pk=id)
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('add_expense_category')

    if category.user != request.user:
        messages.error(request,'Something Went Wrong')
        return redirect('add_expense_category')

    context = {
        'value':category.name,
        'update':True,
        'id':category.id
    }

    if request.method == 'GET': 
        return render(request,'expense_app/expense_category_import.html',context)

    if request.method == 'POST':
        name = request.POST.get('name','')

        context = {
            'value':name,
            'update':True,
            'id':category.id
        }

        if name == '':
            messages.error(request,'Expense Category cannot be empty')
            return render(request,'expense_app/expense_category_import.html',context)
        
        name = name.lower().capitalize()
        if ExpenseCategory.objects.filter(user=request.user,name = name).exists():
            messages.error(request,f'Expense Category ({name}) already exists.')
            return render(request,'expense_app/expense_category_import.html',context)
        
        category.name = name
        category.save()

        messages.success(request,'Expense Category Updated')
        return redirect('add_expense_category')

@login_required(login_url='login')
def delete_expense_category(request,id):

    if ExpenseCategory.objects.filter(id=id,user=request.user).exists():
        category = ExpenseCategory.objects.get(id=id,user=request.user)
        
        if category.user != request.user:
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
    
    if Expense.objects.filter(id=id,user=request.user).exists():
        expense = Expense.objects.get(id=id,user=request.user)
    
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense')
    
    if expense.user != request.user:
        messages.error(request,'Something Went Wrong')
        return redirect('expense')
    
    categories = ExpenseCategory.objects.filter(user=request.user).exclude(id=expense.category.id)

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
        expense = Expense.objects.get(id=id,user=request.user)
        
        if expense.user != request.user:
            messages.error(request,'Something Went Wrong')
            return redirect('expense')
        
        else:
            expense.delete()
            messages.success(request,'Expense Deleted Successfully')
            return redirect('expense')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense')

@login_required(login_url='login')
def download_as_excel(request,filter_by):
    filter_by = str(filter_by)
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses-'+ str(request.user.username) + '-' + str(localtime())+".xls"
    
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
    response['Content-Disposition'] = 'attachment; filename=Expenses-'+ str(request.user.username) + '-' + str(localtime()) + ".csv"
    
    writer = csv.writer(response)
    writer.writerow(['Date','Category','Description','Amount'])
    
    expenses = queryset_filter(User.objects.get(username=request.user.username),filter_by).order_by('date')
    for expense in expenses:
        writer.writerow([expense.date,expense.category.name,expense.description,expense.amount])
    
    writer.writerow(['','','',''])
    writer.writerow(['TOTAL','','',str(expenses.aggregate(Sum('amount'))['amount__sum'])])
    return response

@login_required(login_url='login')
def import_expense(request):
    return render(request,'expense_app/expense_category_import.html',{
        'upload':True
    })

@login_required(login_url='login')
def upload_csv(request):

    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('expense_csv_file')
            
            if csv_file == None:
                messages.error(request,'CSV file required')
                return redirect('import_expense')
                
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'Please Upload a CSV file.')
                return redirect('import_expense')

            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return redirect('import_expense')

            csv = pd.read_csv(csv_file)

            if csv.shape[0] > 10:
                messages.error(request,'Please upload a CSV file with less than 10 rows.')
                return redirect('import_expense')

            csv.columns = [c.lower() for c in csv.columns]

            if ExpenseCategory.objects.filter(user = request.user, name='Loaded From Csv'):
                csv_expense_category = ExpenseCategory.objects.get(user = request.user, name='Loaded From Csv')
            else:
                csv_expense_category = ExpenseCategory.objects.create(user = request.user, name='Loaded From Csv')
                csv_expense_category.save()

            expense_count = 0
            for i,row in csv.iterrows():
                if not pd.isna(row['date']):
                    date = row['date'].split('-')
                    try:
                        date = datetime.date(2000 + int(date[2]) ,int(date[1]),int(date[0]))
                    except:
                        date = datetime.date.today()
                else:
                    date = datetime.date.today()

                if not pd.isna(row['category']):
                    name = row['category'].strip().lower().capitalize()
                    if ExpenseCategory.objects.filter(user = request.user, name = name).exists():
                        category = ExpenseCategory.objects.get(user = request.user, name = name)
                    else:
                        category = ExpenseCategory.objects.create(user = request.user, name = name)
                        category.save()
                else:
                    category = csv_expense_category
                
                if not pd.isna(row['description']):
                    description = row['description'].strip()
                else:
                    description = 'Loaded From Csv'
                
                if not pd.isna(row['amount']):
                    Expense.objects.create(
                        user = request.user,
                        amount = float(row['amount']),
                        date = date,
                        description = description,
                        category = category
                    ).save()
                    expense_count += 1
            
            expense_send_success_mail(request,csv_file.name,expense_count,'CSV')
            messages.success(request,'Expenses are saved from csv file.')
            return redirect('expense')
        
        except Exception as e:
            expense_send_error_mail(request,csv_file.name,'CSV')
            print(repr(e))

            messages.error(request,'Please Check if the format of csv file is correct.')
            return redirect('import_expense')

@login_required(login_url='login')
def upload_excel(request):

    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('expense_excel_file')
            
            if excel_file == None:
                messages.error(request,'Excel file required')
                return redirect('import_expense')
                
            if not (excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx')):
                messages.error(request,'Please Upload a Excel file.')
                return redirect('import_expense')

            if excel_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (excel_file.size/(1000*1000),))
                return redirect('import_expense')
            
            if excel_file.name.endswith('.xls'):
                data = xls_get(excel_file, column_limit=4)
            elif excel_file.name.endswith('.xlsx'):
                data = xlsx_get(excel_file, column_limit=4)
            else:
                messages.error(request,'Please Upload a Excel file.')
                return redirect('import_expense')
            
            keys_excel = list(data.keys())

            expense_excel_data = data[keys_excel[0]]

            try:
                expense_excel_data.remove([])
            except:
                pass

            if len(expense_excel_data) > 11:
                messages.error(request,'Please upload a excel file with less than 10 rows.')
                return redirect('import_expense')

            if ExpenseCategory.objects.filter(user = request.user, name='Loaded From Excel'):
                excel_expense_category = ExpenseCategory.objects.get(user = request.user, name='Loaded From Excel')
            else:
                excel_expense_category = ExpenseCategory.objects.create(user = request.user, name='Loaded From Excel')
                excel_expense_category.save()

            headers = expense_excel_data.pop(0)
            headers = [c.lower() for c in headers] 

            if headers != ['date', 'category', 'description', 'amount']:
                expense_send_error_mail(request,excel_file.name,'Excel')
                messages.error(request,'Please Check if the format of excel file is correct.')
                return redirect('import_expense')

            expense_count = 0
            for row in expense_excel_data:

                if(len(row) != 4):
                    break

                if not row[0] == '':
                    if isinstance(row[0],datetime.date):
                        date = row[0]
                    else:
                        date = row['date'].split('-')
                        try:
                            date = datetime.date(2000 + int(date[2]) ,int(date[1]),int(date[0]))
                        except:
                            date = datetime.date.today()
                else:
                    date = datetime.date.today()

                if not row[1] == '':
                    name = row[1].strip().lower().capitalize()
                    if ExpenseCategory.objects.filter(user = request.user, name = name).exists():
                        category = ExpenseCategory.objects.get(user = request.user, name = name)
                    else:
                        category = ExpenseCategory.objects.create(user = request.user, name = name)
                        category.save()
                else:
                    category = excel_expense_category
                
                if not row[2] == '':
                    description = row[2].strip()
                else:
                    description = 'Loaded From Excel'
                
                if not row[3] == '':
                    Expense.objects.create(
                        user = request.user,
                        amount = float(row[3]),
                        date = date,
                        description = description,
                        category = category
                    ).save()
                    expense_count += 1
            
            expense_send_success_mail(request,excel_file.name,expense_count,'Excel')
            messages.success(request,'Expenses are saved from excel file.')
            return redirect('expense')
        
        except Exception as e:
            expense_send_error_mail(request,excel_file.name,'Excel')
            print(repr(e))

            messages.error(request,'Please Check if the format of excel file is correct.')
            return redirect('import_expense')

@login_required(login_url='login')
def expense_page_sort(request):

    expenses =  Expense.objects.filter(user=request.user)
    base_url = ''

    try:
    
        if 'amount_sort' in request.GET and request.GET.get('amount_sort'):
            base_url = f'?amount_sort={request.GET.get("amount_sort",2)}&'
            if int(request.GET.get('amount_sort',2)) == 1:
                expenses = expenses.order_by('-amount')
            elif int(request.GET.get('amount_sort',2)) == 2:
                expenses = expenses.order_by('amount')
        
        if 'date_sort' in request.GET and request.GET.get('date_sort'):
            base_url = f'?date_sort={request.GET.get("date_sort",2)}&'
            if int(request.GET.get('date_sort',2)) == 1:
                expenses = expenses.order_by('-date')
            elif int(request.GET.get('date_sort',2)) == 2:
                expenses = expenses.order_by('date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('expense')

    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_expenses = Paginator.get_page(paginator,page_number)

    if UserProfile.objects.filter(user = request.user).exists():
        currency = UserProfile.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'

    return render(request,'expense_app/expense.html',{
        'currency':currency,
        'page_expenses':page_expenses,
        'expenses':expenses,
        'base_url':base_url
    })