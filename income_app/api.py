from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from datetime import timedelta
from .models import IncomeSource,Income
import json
from django.db.models import Q

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
        source = IncomeSource.objects.get(user = request.user,source=source)
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

@login_required(login_url='login')
def search_income(request):
    if request.method == 'POST':
        query = json.loads(request.body).get('search_query','')

        if query == '':
            return JsonResponse({
                'error':'Not Found'
            })
        
        user_incomes = Income.objects.filter(user = request.user)

        incomes = user_incomes.filter(
            Q(amount__istartswith = query) | 
            Q(date__istartswith = query) | 
            Q(description__icontains = query) | 
            Q(source__source__icontains = query)
        )
        
        filtered_results = incomes.values('id','amount','description','source__source','date')
		
        return JsonResponse(
            list(filtered_results)
            ,safe=False
        )