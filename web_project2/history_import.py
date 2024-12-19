import os 
import django
# import random
from random import randint
# from datetime import timedelta
# from django.utils import timezone
from django.shortcuts import get_object_or_404
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_project2.settings")
django.setup()

from Movie.models import Movie, View_history, User_rating
from django.contrib.auth.models import User

users = User.objects.all()
movies = Movie.objects.all()

rating_df = pd.read_csv("filtered_rating.csv")

for index, row in rating_df.iterrows():
    movie = get_object_or_404(Movie, id=row['movieId'])
    user = get_object_or_404(User, id=row['userId'])

    View_history.objects.create(user=user, movie=movie, view_time=row['timestamp'])
    User_rating.objects.create(user=user, movie=movie, 
                               rating_time=row['timestamp'], 
                               rating_score=row['rating'])


# for user in users:
#     current_time = timezone.now()
#     num_genres = randint(1,7)
#     # tao danh gia phim cho cac genre ma user yeu thich 
#     favor_genre = []
#     for i in range(num_genres):
#         random_genre = random.choice(genres)
#         favor_genre.append(random_genre)
#         movies_with_random_genre = Movie.objects.filter(genres=random_genre)
#         for movie in movies_with_random_genre:
#             if randint(0,2) != 0:
#                 time_delta = timedelta(days=random.randint(1,1825))
#                 random_time = current_time - time_delta 
#                 View_history.objects.create(user=user, movie=movie, view_time=random_time)
#                 rating = random.choice([5,6,7,8,9,10])
#                 User_rating.objects.create(user=user, movie=movie, rating_time=random_time, rating_score=rating)

#     # tao danh gia phim cho cac genre ma nguoi dung khong yeu thich 
#     unfavor_genre = list(set(genres) - set(favor_genre))
#     for i in range(num_genres):
#         random_genre = random.choice(unfavor_genre)
#         movies_with_random_genre = Movie.objects.filter(genres=random_genre)
#         for movie in movies_with_random_genre:
#             if randint(0,8) == 0:
#                 time_delta = timedelta(days=random.randint(1,1825))
#                 random_time = current_time - time_delta 
#                 View_history.objects.create(user=user, movie=movie, view_time=random_time)
#                 rating = random.choice([1,2,3,4,5,6,7,8])
#                 User_rating.objects.create(user=user, movie=movie, rating_time=random_time, rating_score=rating)








