from django.shortcuts import render
from .models import Movie

# Create your views here.
def movie_view(request):
    movies = Movie.objects.order_by('release_date')
    for movie in movies:
        movie.update_view_count()
        movie.update_rating_score()
    return render(request, 'movie/movie.html', {'movies':movies})



def one_movie(request):
    movie = Movie.objects.first()
    movie.update_view_count()
    movie.update_rating_score()
    return render(request, 'movie/one_movie.html', {'movie':movie})
