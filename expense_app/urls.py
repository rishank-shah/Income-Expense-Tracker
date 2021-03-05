from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.expense_page,name="expense"),
    path('add-expense/',views.add_expense,name="add_expense"),
    path('add-category/',views.add_expense_category,name="add_expense_category"),
    path('delete-category/<int:id>/',views.delete_expense_category,name="delete_expense_category"),
    path('edit-expense/<int:id>/',views.edit_expense,name="edit_expense")
]
