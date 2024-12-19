import os
import django
import pandas as pd
import ast

os.environ.setdefault("DJANGO_SETTINGS_MODULE","movie_web_project.settings")
django.setup()

from movie.models import Genre, Actor, Movie

data = pd.read_csv('movies.csv')
def convert_to_list(json_str):
    try:
        return ast.literal_eval(json_str)
    except (ValueError, SyntaxError):
        return []
# Đọc dữ liệu từ tệp CSV và áp dụng chuyển đổi cho cột 'casts' từ str sang list
data = pd.read_csv('movies.csv', converters={'actors': convert_to_list, 'genres': convert_to_list,})

#loop through each data row
for index, row in data.iterrows():
    m = Movie(
        title=row['title'],
        description=row['description'],
        release_date=row['release_date'],
        duration=row['duration'],
    )
    m.save()

    for genre_name in row['genres']:
        g, created = Genre.objects.get_or_create(name=genre_name)
        m.genres.add(g)

    for actor_name in row['actors']:
        a, created = Actor.objects.get_or_create(name=actor_name)
        m.actors.add(a)

    m.save()


