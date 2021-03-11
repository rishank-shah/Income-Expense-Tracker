from django.shortcuts import render, redirect
from .models import IncomeSource,Income
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from user_profile.models import UserProfile
from django.utils.timezone import localtime
from django.http import HttpResponse
from django.db.models import Sum
import xlwt
from .utils import queryset_filter

@login_required(login_url='login')
def income_page(request):
    incomes =  Income.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(incomes,4)
    page_number = request.GET.get('page')
    page_incomes = Paginator.get_page(paginator,page_number)
    if UserProfile.objects.filter(user = request.user).exists():
        currency = UserProfile.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'
    return render(request,'income_app/income.html',{
        'currency':currency,
        'page_incomes':page_incomes,
        'incomes':incomes
    })

@login_required(login_url='login')
def add_income(request):
    if IncomeSource.objects.filter(user=request.user).exists():
        sources = IncomeSource.objects.filter(user=request.user)
        context = {
            'sources' : sources,
            'values':request.POST
    	}
        if request.method == 'GET':
            return render(request,'income_app/add_income.html',context)
        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            source = request.POST.get('source','')
            date = request.POST.get('income_date','')
            if amount == '':
                messages.error(request,'Amount cannot be empty')
                return render(request,'income_app/add_income.html',context)
            amount = float(amount)
            if amount<=0 :
                messages.error(request,'Amount should be greater than zero')
                return render(request,'income_app/add_income.html',context)
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'income_app/add_income.html',context)
            if source == '':
                messages.error(request,'IncomeSource cannot be empty')
                return render(request,'income_app/add_income.html',context)
            if date == '':
                date = localtime()
            source_obj = IncomeSource.objects.get(user=request.user,source =source)
            Income.objects.create(
                user=request.user,
                amount=amount,
                date=date,
                description=description,
                source=source_obj
            ).save()
            messages.success(request,'Income Saved Successfully')
            return redirect('income')
    else:
        messages.error(request,'Please add a income source first.')
        return redirect('add_income_source')

@login_required(login_url='login')
def add_income_source(request):
    sources = IncomeSource.objects.filter(user=request.user)
    context = {
        'sources' : sources,
        'values':request.POST
    }
    if request.method == 'GET': 
        return render(request,'income_app/add_income_source.html',context)
    if request.method == 'POST':
        source = request.POST.get('source','')
        if source == '':
            messages.error(request,'IncomeSource cannot be empty')
            return render(request,'income_app/add_income_source.html',context)
        source = source.lower().capitalize()
        if IncomeSource.objects.filter(user=request.user,source = source).exists():
            messages.error(request,f'Income Source ({source}) already exists.')
            return render(request,'income_app/add_income_source.html',context)
        IncomeSource.objects.create(user=request.user,source = source).save()
        messages.success(request,'IncomeSource added')
        return render(request,'income_app/add_income_source.html',{
            'sources' : sources
        })

@login_required(login_url='login')
def delete_income_source(request,id):
    if IncomeSource.objects.filter(pk=id).exists():
        income_source = IncomeSource.objects.get(pk=id)
        user = User.objects.get(username=request.user.username)
        if income_source.user != user:
            messages.error(request,'You cannot delete this income source.')
            return redirect('add_income_source')
        else:
            income_source.delete()
            messages.success(request,'Deleted income source')
            return redirect('add_income_source')
    messages.error(request,'Please try again')
    return redirect('add_income_source')

@login_required(login_url='login')
def edit_income(request,id):
    sources = IncomeSource.objects.filter(user=request.user)
    if Income.objects.filter(id=id,user=request.user).exists():
        income = Income.objects.get(id=id,user=request.user)
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('income')
    context = {
        'income':income,
        'values': income,
        'sources':sources
    }
    if request.method == 'GET':
        return render(request,'income_app/edit_income.html',context)

    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        source = request.POST.get('source','')
        date = request.POST.get('income_date','')
        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'income_app/edit_income.html',context)
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'income_app/edit_income.html',context)
        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'income_app/edit_income.html',context)
        if source == '':
            messages.error(request,'Income Source cannot be empty')
            return render(request,'income_app/edit_income.html',context)
        if date == '':
            date = localtime()
        income_obj = IncomeSource.objects.get(user=request.user,source=source)
        income.amount = amount
        income.date = date
        income.source = income_obj
        income.description = description
        income.save() 
        messages.success(request,'Income Updated Successfully')
        return redirect('income')

@login_required(login_url='login')
def delete_income(request,id):
    if Income.objects.filter(id=id,user=request.user).exists():
        Income.objects.get(id=id,user=request.user).delete()
        messages.success(request,'Income Deleted Successfully')
        return redirect('income')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('income')

@login_required(login_url='login')
def download_as_excel(request,filter_by):
    filter_by = str(filter_by)
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes-'+ str(request.user.username) + str(localtime())+".xls"
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes')
    if filter_by != '':
        ws.write(0,0,f"Incomes in {filter_by.lower().capitalize()}")
    else:
        ws.write(0,0,f"Incomes in Year")
    row_number = 1
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True
    columns = ['Date','Source','Description','Amount']
    for col_num in range(len(columns)):
        ws.write(row_number,col_num,columns[col_num],fontStyle)
    fontStyle = xlwt.XFStyle()
    incomes = queryset_filter(User.objects.get(username=request.user.username),filter_by).order_by('date')
    rows = incomes.values_list('date','source__source','description','amount')
    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            ws.write(row_number,col_num,str(row[col_num]),fontStyle)
    row_number +=2
    style = xlwt.easyxf('font: colour red, bold True;')
    ws.write(row_number,0,'TOTAL',style)
    ws.write(row_number,3,str(incomes.aggregate(Sum('amount'))['amount__sum']),style)
    wb.save(response)
    return response