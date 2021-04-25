import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')
django.setup()

from django.contrib.auth.models import User
from expense_app.models import (
    Expense,
    ExpenseCategory
)
from income_app.models import (
    Income,
    IncomeSource
)
from user_profile.models import UserProfile
from datetime import datetime,timedelta
from random import randint
from django.utils.timezone import localtime


user = None


def genarate_test_user():
    global user
    user_dict = {}
    print()
    user_dict["username"] = input('Enter username of testing account: ')
    user_dict["first_name"] = input('Enter first_name of testing account: ')
    user_dict["last_name"] = input('Enter last_name of testing account: ')
    user_dict["email"] = input('Enter email of testing account: ')
    password = input('Enter password of testing account: ')

    print()

    for key,value in user_dict.items():
        print(f'\t{key} : {value}')
    
    print()
    ans =  input('Do you want to continue with this information? (y/n): ')
    print()

    if(ans.lower() == 'y'):
        try:

            user = User.objects.create_user(
                username = user_dict["username"],
                first_name = user_dict["first_name"],
                last_name = user_dict["last_name"],
                email = user_dict["email"], 
            )
            user.set_password(password)
            user.is_active = True
            user.save()
            print(f'[INFO] Created User - {user.username}')
            UserProfile.objects.create(user = user).save()

        except Exception as e:
            sys.exit(f'[ERROR](while creating user) {repr(e)}')
    else:
        sys.exit('[ERROR] User cancelled operation')


def generate_expense_category():
    global user
    categories = ['Food','Other','Rent','Shopping']

    if not user:
        sys.exit('[ERROR] Something went wrong')

    for i in categories:
        ExpenseCategory.objects.create(user = user,name=i)
    
    print('[INFO] Created Expense Categories')


def generate_income_category():
    global user
    sources = ['Business','Other','Salary','Misc']

    if not user:
        sys.exit('[ERROR] Something went wrong')

    for i in sources:
        IncomeSource.objects.create(user = user,source = i)
    
    print('[INFO] Created Income Sources')


def generate_expenses():
    global user
    category = ExpenseCategory.objects.filter(user = user)
    
    # Generate Today's Expense
    today_date = datetime.today()
    today_date_time = localtime()
    print("[INFO] Generating Today's Expense")
    for i in category:
        expense = Expense.objects.create(
            user=user,
            amount = randint(1000,5000),
            date = today_date,
            description = 'Loaded from Test Script',
            category = i
        )
        expense.created_at = today_date_time
        expense.save()

    # Generate This Week's Expense
    week_date_time = today_date - timedelta(days=7) 
    print("[INFO] Generating This Week's Expense")
    for i in category:
        week_date_time_obj = week_date_time + timedelta(days=randint(1,4))
        expense = Expense.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = week_date_time_obj,
            description = 'Loaded from Test Script',
            category = i
        )
        expense.created_at = today_date_time
        expense.save()

    # Generate This Month's Expense
    month_date_time = today_date 
    print("[INFO] Generating This Month's Expense")
    for i in category:
        month_date_time = month_date_time.replace(day=randint(1,30))
        expense = Expense.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = month_date_time,
            description = 'Loaded from Test Script',
            category = i
        )
        expense.created_at = today_date_time
        expense.save()
    
    # Generate This Year's Expense
    year_date_time = today_date 
    print("[INFO] Generating This Year's Expense")
    for i in category:
        year_date_time = year_date_time.replace(month=randint(1,today_date_time.month),day=randint(1,30))
        expense = Expense.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = year_date_time,
            description = 'Loaded from Test Script',
            category = i
        )
        expense.created_at = today_date_time
        expense.save()


def generate_incomes():
    global user
    source = IncomeSource.objects.filter(user = user)
    
    # Generate Today's Income
    today_date = datetime.today()
    today_date_time = localtime()
    print("[INFO] Generating Today's Income")
    for i in source:
        income = Income.objects.create(
            user=user,
            amount = randint(1000,5000),
            date = today_date,
            description = 'Loaded from Test Script',
            source = i
        )
        income.created_at = today_date_time
        income.save()

    # Generate This Week's Income
    week_date_time = today_date - timedelta(days=7) 
    print("[INFO] Generating This Week's Income")
    for i in source:
        week_date_time_obj = week_date_time + timedelta(days=randint(1,4))
        income = Income.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = week_date_time_obj,
            description = 'Loaded from Test Script',
            source = i
        )
        income.created_at = today_date_time
        income.save()

    # Generate This Month's Income
    month_date_time = today_date 
    print("[INFO] Generating This Month's Income")
    for i in source:
        month_date_time = month_date_time.replace(day=randint(1,30))
        income = Income.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = month_date_time,
            description = 'Loaded from Test Script',
            source = i
        )
        income.created_at = today_date_time
        income.save()
    
    # Generate This Year's Income
    year_date_time = today_date 
    print("[INFO] Generating This Year's Income")
    for i in source:
        year_date_time = year_date_time.replace(month=randint(1,today_date_time.month),day=randint(1,30))
        income = Income.objects.create(
            user = user,
            amount = randint(1000,5000),
            date = year_date_time,
            description = 'Loaded from Test Script',
            source = i
        )
        income.created_at = today_date_time
        income.save()

if __name__ == "__main__":
    print('[INFO] Starting Script')
    print('[INFO] Generating User')
    genarate_test_user()
    print('[INFO] Generating Expense Categories')
    generate_expense_category()
    print('[INFO] Generating Income Sources')
    generate_income_category()
    print('[INFO] Generating Expenses')
    generate_expenses()
    print('[INFO] Generating Incomes')
    generate_incomes()
    sys.exit('[INFO] Generated all data')
