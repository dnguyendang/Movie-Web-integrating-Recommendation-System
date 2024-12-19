from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Genre, Production_country, User_rating, View_history
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def Movies_view(request):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movies = Movie.objects.all().order_by('release_date').reverse()
    paginator = Paginator(movies, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Movie/movies.html', {'genres':genres, 'countries':countries,'movies':movies, 'page_obj': page_obj})

def Movie_trailer_view(request, movie_id):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    user_rating = None

    if user.is_authenticated:
        #Check if the user has already rated the movie 
        user_rating = User_rating.objects.filter(user=user, movie=movie).first()
        View_history.objects.create(user=user, movie=movie)

    if request.method == "GET":
        rate = request.GET.get('rate')

        #Only update or add a new rating when the user clicks "Post"
        if rate and user.is_authenticated:
            if user_rating:
                #If the user has already rated the movie, update the existing rating
                user_rating.rating_score = rate
                # thoi gian ko tu cap nhat sau khi save ... can dieu chinh thgian 
                user_rating.save()
            else:
                User_rating.objects.create(user=user, movie=movie, rating_score=rate)

    return render(request, 'Movie/movie_trailer.html', {'movie':movie, 'user':user, 'genres':genres, 'countries':countries, 'user_rating':user_rating})

def Movie_details_view(request, movie_id):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    user_rating = None
    if user.is_authenticated:
        #Check if the user has already rated the movie 
        user_rating = User_rating.objects.filter(user=user, movie=movie).first()

    return render(request, 'Movie/movie_details.html', {'movie':movie, 'user':user, 'genres':genres, 'countries':countries, 'user_rating':user_rating})

def Movies_by_genre_view(request, genre_id):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    genre = get_object_or_404(Genre, id=genre_id)
    movies_by_genre = Movie.objects.filter(genres=genre).order_by('release_date').reverse()
    paginator = Paginator(movies_by_genre, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Movie/movies_by_genre.html', {'genres':genres, 'countries':countries,'page_obj':page_obj, 'genre_main':genre})

def Movies_by_country_view(request, country_id):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    country = get_object_or_404(Production_country, id=country_id)
    movies_by_country = Movie.objects.filter(production_countries=country).order_by('release_date').reverse()
    paginator = Paginator(movies_by_country, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Movie/movies_by_country.html', {'genres':genres, 'countries':countries,'page_obj':page_obj, 'country_main':country})

def Movies_by_popularity_view(request):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movies_by_popularity = Movie.objects.all().order_by('popularity').reverse()
    paginator = Paginator(movies_by_popularity, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Movie/movies_by_popularity.html', {'genres':genres, 'countries':countries,'page_obj':page_obj})

def Movies_by_rate_view(request):
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movies_by_rate = Movie.objects.all().order_by('rating_score').reverse()
    paginator = Paginator(movies_by_rate, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Movie/movies_by_rate.html', {'genres':genres, 'countries':countries,'page_obj':page_obj})
