from django.urls import path
from . import views

urlpatterns = [
    path('profile/',views.profile,name="user_profile"),
    path('change-currency/',views.save_currency,name="change_currency")
]
