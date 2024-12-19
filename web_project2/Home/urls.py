from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_view, name='Home'),
    path('user_profile/', views.UserProfile_view, name='UserProfile'),
    path('change_password/', views.Change_password, name='ChangePassword'),
    path('info/', views.Info_view, name='Info'),
    
]