from django.urls import path
from . import views, api
from django.views.generic import TemplateView

urlpatterns = [
    path('view/',views.expense_page,name="expense"),
    path('expense-sort/',views.expense_page_sort,name="expense_page_sort"),
    path('add-expense/',views.add_expense,name="add_expense"),
    path('add-category/',views.add_expense_category,name="add_expense_category"),
    path('edit-category/<int:id>/',views.edit_expense_category,name="edit_expense_category"),
    path('delete-category/<int:id>/',views.delete_expense_category,name="delete_expense_category"),
    path('edit-expense/<int:id>/',views.edit_expense,name="edit_expense"),
    path('delete-expense/<int:id>/',views.delete_expense,name="delete_expense"),
    path('expense-summary-data',api.expense_summary,name="expense_summary_data"),
    path('expense-summary/',TemplateView.as_view(template_name="expense_app/expense_summary.html"),name="expense_summary"),
    path('download-excel/<str:filter_by>',views.download_as_excel,name = 'download_as_excel'),
    path('download-csv/<str:filter_by>',views.download_as_csv,name = 'download_as_csv'),
    path('search',api.search_expense,name="expense_search"),
    path('import/',views.import_expense,name="import_expense"),
    path('expense-import-from-csv',views.upload_csv,name="expense_import_from_csv"),
    path('expense-import-from-excel',views.upload_excel,name="expense_import_from_excel")
]
