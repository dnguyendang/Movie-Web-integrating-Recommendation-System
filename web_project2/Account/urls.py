from django.urls import path
from . import views

urlpatterns = [
    # path('account/', views.Account_view, name='Account'),
    path('login/', views.Login_view, name='Login'),
    path('register/', views.Register_view, name='Register'),
    path('logout/', views.Logout_view, name='Logout'),
]