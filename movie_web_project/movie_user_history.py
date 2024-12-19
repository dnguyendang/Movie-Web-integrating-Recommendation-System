import os 
import django
import random
from random import randint
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE","movie_web_project.settings")
django.setup()

from movie.models import Movie, Genre, View_history, User_rating
from django.contrib.auth.models import User

users = User.objects.all()
genres = Genre.objects.all()


for user in users:
    current_time = timezone.now()
    num_genres = randint(1,7)
    # tao danh gia phim cho cac genre ma user yeu thich 
    favor_genre = []
    for i in range(num_genres):
        random_genre = random.choice(genres)
        favor_genre.append(random_genre)
        movies_with_random_genre = Movie.objects.filter(genres=random_genre)
        for movie in movies_with_random_genre:
            if randint(0,2) != 0:
                time_delta = timedelta(days=random.randint(1,1825))
                random_time = current_time - time_delta 
                View_history.objects.create(user=user, movie=movie, view_time=random_time)
                rating = random.choice([5,6,7,8,9,10])
                User_rating.objects.create(user=user, movie=movie, rating_time=random_time, rating_score=rating)

    # tao danh gia phim cho cac genre ma nguoi dung khong yeu thich 
    unfavor_genre = list(set(genres) - set(favor_genre))
    for i in range(num_genres):
        random_genre = random.choice(unfavor_genre)
        movies_with_random_genre = Movie.objects.filter(genres=random_genre)
        for movie in movies_with_random_genre:
            if randint(0,8) == 0:
                time_delta = timedelta(days=random.randint(1,1825))
                random_time = current_time - time_delta 
                View_history.objects.create(user=user, movie=movie, view_time=random_time)
                rating = random.choice([1,2,3,4,5,6,7,8])
                User_rating.objects.create(user=user, movie=movie, rating_time=random_time, rating_score=rating)







