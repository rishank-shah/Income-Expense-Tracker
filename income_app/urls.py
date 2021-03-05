from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.income_page,name="income"),
    path('add-income/',views.add_income,name="add_income"),
    path('add-source/',views.add_income_source,name="add_income_source"),
    path('delete-income-source/<int:id>/',views.delete_income_source,name="delete_income_source")
]
