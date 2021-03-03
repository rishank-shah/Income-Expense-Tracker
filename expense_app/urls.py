from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('view/',views.expense_page,name="expense"),
    path('add-expense/',views.add_expense,name="add_expense")
]
