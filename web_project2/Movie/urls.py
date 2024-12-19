from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.Movies_view, name='Movies'),
    path('movies/<int:movie_id>/', views.Movie_details_view, name='Movie_details'),
    path('movies/<int:movie_id>/trailer', views.Movie_trailer_view, name='Movie_trailer'),
    path('genres/<int:genre_id>/', views.Movies_by_genre_view, name="Movies_by_genre"),
    path('countries/<int:country_id>/', views.Movies_by_country_view, name="Movies_by_country"),
    path('movies_popularity/', views.Movies_by_popularity_view, name='Movies_popularity'),
    path('movies_rata', views.Movies_by_rate_view, name='Movies_rate'),
]
