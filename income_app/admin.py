from django.contrib import admin
from .models import Income, IncomeSource

admin.site.register(IncomeSource)
admin.site.register(Income)