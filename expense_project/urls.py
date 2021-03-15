"""expense_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"),name="index"),
    path('download-data/', TemplateView.as_view(template_name="download_data.html"),name="download_data"),
    path('download-data/complete-spreadsheet/excel',views.complete_spreadsheet_excel,name="complete_spreadsheet_excel"),
    path('download-data/complete-spreadsheet/csv',views.complete_spreadsheet_csv,name="complete_spreadsheet_csv"),
    path('download-data/complete-spreadsheet/pdf',views.complete_spreadsheet_pdf,name="complete_spreadsheet_pdf"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('auth/',include('auth_app.urls')),
    path('expense/',include('expense_app.urls')),
    path('income/',include('income_app.urls')),
    path('user/',include('user_profile.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

admin.site.site_header = 'Expense Income Tracker Admin'
admin.site.index_title = 'Expense-Income-Tracker'