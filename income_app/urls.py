from django.urls import path
from . import views,api
from django.views.generic import TemplateView

urlpatterns = [
    path('view/',views.income_page,name="income"),
    path('income-sort/',views.income_page_sort,name="income_page_sort"),
    path('add-income/',views.add_income,name="add_income"),
    path('add-source/',views.add_income_source,name="add_income_source"),
    path('edit-source/<int:id>/',views.edit_income_source,name="edit_income_source"),
    path('delete-income-source/<int:id>/',views.delete_income_source,name="delete_income_source"),
    path('edit-income/<int:id>/',views.edit_income,name="edit_income"),
    path('delete-income/<int:id>/',views.delete_income,name="delete_income"),
    path('income-summary-data',api.income_summary,name="income_summary_data"),
    path('income-summary/',TemplateView.as_view(template_name="income_app/income_summary.html"),name="income_summary"),
    path('download-excel/<str:filter_by>',views.download_as_excel,name = 'income_download_as_excel'),
    path('download-csv/<str:filter_by>',views.download_as_csv,name = 'income_download_as_csv'),
    path('search',api.search_income,name="income_search"),
    path('import/',views.import_income,name="import_income"),
    path('income-import-from-csv',views.upload_csv,name="income_import_from_csv"),
    path('income-import-from-excel',views.upload_excel,name="income_import_from_excel")
]
