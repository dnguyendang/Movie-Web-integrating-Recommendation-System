import os 
import django
import pandas as pd
import ast

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_project2.settings")
django.setup()

from Movie.models import Cast, Genre, Production_company, Production_country, Spoken_language, Movie

def convert_to_list(json_str):
    try:
        return ast.literal_eval(json_str)
    except (ValueError, SyntaxError):
        return []
# Đọc dữ liệu từ tệp CSV và áp dụng chuyển đổi cho cột 'casts' từ str sang list
data = pd.read_csv('tmdb_movie.csv', converters={'casts': convert_to_list, 'genres': convert_to_list, 'production_companies': convert_to_list, 'production_countries': convert_to_list, 'spoken_languages': convert_to_list,})

for index, row in data.iterrows():
    m = Movie(
        backdrop_path = row['backdrop_path'],
        budget = row['budget'],
        # genres = row['genres'],
        overview = row['overview'],
        poster_path = row['poster_path'],
        # production_companies = row['production_companies'],
        # production_countries = row['production_countries'],
        release_date = row['release_date'],
        revenue = row['revenue'],
        runtime = row['runtime'],
        # spoken_languages = row['spoken_languages'],
        tagline = row['tagline'],
        title = row['title'],
        vote_average = row['vote_average'],
        vote_count = row['vote_count'],
        trailer_link = row['trailer_link'],
        # casts = row['casts'],
    )
    m.save()
    for production_company in row['production_companies']:
        p, created = Production_company.objects.get_or_create(name=production_company)
        m.production_companies.add(p)
    for production_country in row['production_countries']:
        p1, created = Production_country.objects.get_or_create(name=production_country)
        m.production_countries.add(p1)
    for genre in row['genres']:
        g, created = Genre.objects.get_or_create(name=genre)
        m.genres.add(g)
    for spoken_language in row['spoken_languages']:
        s, created = Spoken_language.objects.get_or_create(name=spoken_language)
        m.spoken_languages.add(s)
    for cast in row['casts']:
        name=cast.get('name')
        profile_path=cast.get('profile_path','')
        c, created = Cast.objects.get_or_create(name=name, profile_path=profile_path)
        m.casts.add(c)
