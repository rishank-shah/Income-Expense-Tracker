from django.urls import path
from .views import Registration,Login,Logout,Verification
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',Registration.as_view(),name = 'register'),
    path('login/', Login.as_view(), name="login"), 
    path('activate-account/<uidb64>/<token>',Verification.as_view(),name = 'activate'),
    path('logout', Logout.as_view(), name="logout"), 
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name="auth_app/reset_password.html"),name="password_reset"),
    path('reset-password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="auth_app/reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="auth_app/set_new_password.html"),name="password_reset_confirm"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="auth_app/reset_password_done.html"),name="password_reset_complete"),
]
