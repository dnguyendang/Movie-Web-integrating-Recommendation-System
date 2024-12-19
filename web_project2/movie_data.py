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
data = pd.read_csv('movies_data.csv', index_col=0, converters={'genres':convert_to_list, 
                                                            'production_companies':convert_to_list,
                                                            'production_countries':convert_to_list,
                                                            'spoken_languages':convert_to_list,
                                                            'casts':convert_to_list})

# data = pd.read_csv('movies_data_2.csv', index_col=0, converters={'genres':convert_to_list, 
#                                                             'production_companies':convert_to_list,
#                                                             'production_countries':convert_to_list,
#                                                             'spoken_languages':convert_to_list,
#                                                             'casts':convert_to_list})

for index, row in data.iterrows():
    m = Movie(
        id = row['id_movie'],
        backdrop_path = row['backdrop_path'],
        budget = row['budget'],
        # genres = row['genres'],
        overview = row['overview'],
        #popularity
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
        p_com, created = Production_company.objects.get_or_create(id = production_company.get('id'), 
                                                              defaults ={'name':production_company.get('name'), 
                                                              'origin_country':production_company.get('origin_country'),
                                                              'logo_path':production_company.get('logo_path')})
        m.production_companies.add(p_com)

    for production_country in row['production_countries']:
        p_coun, created = Production_country.objects.get_or_create(iso_3166_1=production_country.get('iso_3166_1'),
                                                                   name=production_country.get('name'))
        m.production_countries.add(p_coun)

    for spoken_language in row['spoken_languages']:
        s, created = Spoken_language.objects.get_or_create(english_name=spoken_language.get('english_name'),
                                                           name=spoken_language.get('name'),
                                                           iso_639_1=spoken_language.get('iso_639_1'))
        m.spoken_languages.add(s)     
    
    for genre in row['genres']:
        g, created = Genre.objects.get_or_create(id=genre.get('id'),
                                                 name=genre.get('name'))
        m.genres.add(g)

    for cast in row['casts']:
        c, created = Cast.objects.get_or_create(id = cast.get('cast_id'),
                                                defaults={'gender': cast.get('gender'),
                                                'name':cast.get('name'), 
                                                'profile_path':cast.get('profile_path')})
        m.casts.add(c)
