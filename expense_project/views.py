from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expense_app.models import Expense
from income_app.models import Income
from datetime import timedelta
from django.db.models import Sum
from django.http import HttpResponse
import xlwt
import csv
from django.utils.timezone import localtime
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from user_profile.models import UserProfile
import datetime

@login_required(login_url='login')
def dashboard(request):
    today_date_time = localtime()
    today_date = datetime.date.today()
    week_date_time = today_date - timedelta(days=7) 
    start_today_data = today_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today_data = today_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)

    incomes_today_display = Income.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')
    expenses_today_display = Expense.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')

    expenses_year = Expense.objects.filter(user=request.user,date__year=today_date.year)
    expenses_month = expenses_year.filter(date__month=today_date.month)
    expenses_today = expenses_month.filter(date__exact=today_date)
    expenses_week = expenses_month.filter(date__gte=week_date_time)

    spent_year_count = expenses_year.count()
    spent_month_count = expenses_month.count()
    spent_today_count = expenses_today.count()
    spent_week_count = expenses_week.count()
    spent_month = expenses_month.aggregate(Sum('amount'))
    spend_today = expenses_today.aggregate(Sum('amount'))
    spent_week = expenses_week.aggregate(Sum('amount'))
    spent_year = expenses_year.aggregate(Sum('amount'))

    return render(request,'dashboard.html',{
        'expenses':expenses_today_display[:5],
        'incomes':incomes_today_display[:5],
        'spent_today':spend_today['amount__sum'],
        'spent_today_count':spent_today_count,
        'spent_month':spent_month['amount__sum'],
        'spent_month_count':spent_month_count,
        'spent_year':spent_year['amount__sum'],
        'spent_year_count':spent_year_count,
        'spent_week':spent_week['amount__sum'],
        'spent_week_count':spent_week_count,
    })

@login_required(login_url='login')
def complete_spreadsheet_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes-Expenses-'+ str(request.user.username) + '-' + str(localtime())+".xls"

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('All Data')

    row_number = 1
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True
    columns = ['Date','Source','Category','Description','Amount In', 'Amount Out']
    for col_num in range(len(columns)):
        ws.write(row_number,col_num,columns[col_num],fontStyle)

    fontStyle = xlwt.XFStyle()
    incomes = Income.objects.filter(user=request.user).order_by('date')
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    income_list = incomes.values_list('date','source__source','description','amount')
    expense_list = expenses.values_list('date','category__name','description','amount')
    rows = income_list

    for row in rows:
        row_number += 1
        ws.write(row_number,0,str(row[0]),fontStyle)
        ws.write(row_number,1,str(row[1]),fontStyle)
        ws.write(row_number,3,str(row[2]),fontStyle)
        ws.write(row_number,4,str(row[3]),fontStyle)
    
    row_number += 1
    rows = expense_list
    for row in rows:
        row_number += 1
        ws.write(row_number,0,str(row[0]),fontStyle)
        ws.write(row_number,2,str(row[1]),fontStyle)
        ws.write(row_number,3,str(row[2]),fontStyle)
        ws.write(row_number,5,str(row[3]),fontStyle)
    
    row_number +=2
    style = xlwt.easyxf('font: colour red, bold True;')
    ws.write(row_number,0,'TOTAL',style)
    ws.write(row_number,6,'Balance',style)
    style = xlwt.easyxf('font: colour black, bold True;')
    income_total = incomes.aggregate(Sum('amount'))['amount__sum']
    expense_total = expenses.aggregate(Sum('amount'))['amount__sum']

    if expense_total == None:
        balance = income_total
    elif income_total == None:
        balance = -expense_total
    else:
        balance = income_total - expense_total
    
    ws.write(row_number,4,str(income_total),style)
    ws.write(row_number,5,str(expense_total),style)
    style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;''font: colour red, bold True;')
    ws.write(row_number,7,str(balance),style)
    wb.save(response)
    return response

@login_required(login_url='login')
def complete_spreadsheet_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes-Expenses-'+ str(request.user.username) + "-" + str(localtime()) + ".csv"
    
    writer = csv.writer(response)
    writer.writerow(['Date','Source','Category','Description','Amount In', 'Amount Out'])
    incomes = Income.objects.filter(user=request.user).order_by('date')
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    income_list = incomes.values_list('date','source__source','description','amount')
    expense_list = expenses.values_list('date','category__name','description','amount')
    writer.writerow(['','','',''])

    for income in incomes:
        writer.writerow([income.date,income.source.source,'',income.description,income.amount])
    writer.writerow(['','','',''])

    for expense in expenses:
        writer.writerow([expense.date,'',expense.category.name,'',expense.description,'',expense.amount])
    writer.writerow(['','','',''])

    income_total = incomes.aggregate(Sum('amount'))['amount__sum']
    expense_total = expenses.aggregate(Sum('amount'))['amount__sum']

    if expense_total == None:
        balance = income_total
    elif income_total == None:
        balance = -expense_total
    else:
        balance = income_total - expense_total

    writer.writerow(['TOTAL','','','',income_total,expense_total,'BALANCE',str(balance)])
    return response

@login_required(login_url='login')
def complete_spreadsheet_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Incomes-Expenses-'+ str(request.user.username) + '-' + str(localtime()) + ".pdf"
    response['Content-Transfer-Encoding'] = 'binary'

    profile_pic = None
    currency = 'INR'
    if UserProfile.objects.filter(user=request.user).exists():
        user_profile = UserProfile.objects.get(user=request.user)
        profile_pic = user_profile.profile_pic
        currency = user_profile.currency[:3]

    expenses = Expense.objects.filter(user=request.user).order_by('date')
    incomes = Income.objects.filter(user=request.user).order_by('date')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum']
    total_income = incomes.aggregate(Sum('amount'))['amount__sum']
    
    if total_expense == None:
        balance = total_income
    elif total_income == None:
        balance = -total_expense
    else:
        balance = total_income - total_expense

    html_string = render_to_string('partials/_pdf_output.html',{
        'title':'Income Expense List',
        'profile_pic':profile_pic,
        'expenses':expenses,
        'incomes':incomes,
        'total_expense':total_expense,
        'total_income':total_income,
        'currency':currency,
        'balance':balance,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'username':request.user.username,
    })
    
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as pdf_output:
        pdf_output.write(result)
        pdf_output.flush()

        output = open(pdf_output.name,'rb')
        response.write(output.read())
    return response