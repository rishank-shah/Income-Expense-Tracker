from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('profile/',views.profile,name="user_profile"),
    path('change-currency/',views.save_currency,name="change_currency"),
    path('change-password/',views.change_password,name="password_change"),
    path('change-email-pref',views.change_email_pref,name="change_email_pref")
]
