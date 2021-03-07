from django.shortcuts import render, redirect
from .models import IncomeSource,Income
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from user_profile.models import UserProfile
from django.utils.timezone import localtime
import datetime
from django.http import JsonResponse
from datetime import timedelta

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
        income.category = income_obj
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
def income_summary(request):
    today_date = datetime.date.today()
    filter_by = request.GET.get('filter', None)
    if filter_by != None:
        if filter_by.lower() == 'week':
            date_search =  today_date - timedelta(days=7) 
            incomes = Income.objects.filter(user=request.user,date__gte=date_search)
            title = 'Incomes per source in this week'
        elif filter_by.lower() == 'month':
            incomes = Income.objects.filter(user=request.user,date__year=today_date.year,date__month=today_date.month)
            title = 'Incomes per source in this month'
        elif filter_by.lower() == 'year':
            incomes = Income.objects.filter(user=request.user,date__year=today_date.year)
            title = 'Incomes per source in this year'
        elif filter_by.lower() == 'today':
            incomes = Income.objects.filter(user=request.user,date__exact=today_date)
            title = 'Incomes per source earned today'
        else:
            six_months_ago = today_date - datetime.timedelta(days = 30*6)
            incomes = Income.objects.filter(user = request.user,date__gte=six_months_ago)
            title = 'Incomes per source in last six months'
    else:
        six_months_ago = today_date - datetime.timedelta(days = 30*6)
        incomes = Income.objects.filter(user = request.user,date__gte=six_months_ago)
        title = 'Incomes per source in last six months'
    final_rep = {}
    def get_source(income):
        return income.source.source
    source_list = list(set(map(get_source,incomes)))
    def get_income_source_amount(source):
        amount = 0
        source = IncomeSource.objects.get(source=source)
        filtered_by_source = incomes.filter(source=source.id)
        for i in filtered_by_source:
            amount += i.amount
        return amount
    for x in incomes:
        for y in source_list :
            final_rep[y] = get_income_source_amount(y)
    return JsonResponse({
        'income_source_data':final_rep,
        'label_title':title
    },safe=False)