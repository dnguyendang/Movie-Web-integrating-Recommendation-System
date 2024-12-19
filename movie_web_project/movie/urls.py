from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.movie_view, name='movie'),
    path('one_movie/', views.one_movie, name='one_movie'),
] 