from django.contrib import admin
from .models import ExpenseCategory, Expense

admin.site.register(ExpenseCategory)
admin.site.register(Expense)