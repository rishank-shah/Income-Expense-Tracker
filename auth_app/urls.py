from django.urls import path
from .views import Registration,Login,Logout

urlpatterns = [
    path('register/',Registration.as_view(),name = 'register'),
    path('login/', Login.as_view(), name="login"), 
    path('logout', Logout.as_view(), name="logout"), 
]
