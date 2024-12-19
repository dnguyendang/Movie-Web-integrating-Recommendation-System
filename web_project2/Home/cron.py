from django_cron import CronJobBase, Schedule
from .models import PersonalRecommendModel,UserRecommendModel
from Movie.models import User_rating, View_history, Movie, Cast, Genre, Production_company, Production_country, Spoken_language
from django.contrib.auth.models import User

#import libraries
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import operator 
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

class UpdateRecommendCronJob(CronJobBase):
    RUN_EVERY_MINS = 0 #1440 # once a day
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'RecommendModel.update_recommend_cron_job'

    def do(self):
        # delete old recommend data 
        PersonalRecommendModel.objects.all().delete()
        UserRecommendModel.objects.all().delete()

        # retrieve tables 
        user = pd.DataFrame.from_records(User.objects.values())
        cast = pd.DataFrame.from_records(Cast.objects.values())
        genre = pd.DataFrame.from_records(Genre.objects.values())
        movie = pd.DataFrame.from_records(Movie.objects.values())
        production_company = pd.DataFrame.from_records(Production_company.objects.values())
        production_country = pd.DataFrame.from_records(Production_country.objects.values())
        spoken_language = pd.DataFrame.from_records(Spoken_language.objects.values())
        user_rating = pd.DataFrame.from_records(User_rating.objects.values())
        view_history = pd.DataFrame.from_records(View_history.objects.values())

        movie_cast = pd.DataFrame.from_records(Movie.casts.through.objects.all().values('id', 'movie_id', 'cast_id'))
        movie_genre = pd.DataFrame.from_records(Movie.genres.through.objects.all().values('id', 'movie_id', 'genre_id'))
        movie_production_company = pd.DataFrame.from_records(Movie.production_companies.through.objects.all().values('id', 'movie_id', 'production_company_id'))
        movie_production_country = pd.DataFrame.from_records(Movie.production_countries.through.objects.all().values('id', 'movie_id', 'production_country_id'))
        movie_spoken_languages = pd.DataFrame.from_records(Movie.spoken_languages.through.objects.all().values('id', 'movie_id', 'spoken_language_id'))
        
        pivot_movie_genre = movie_genre.pivot_table(index=['movie_id'], columns=['genre_id'], values=['id'], fill_value=0)
        pivot_movie_genre = pd.DataFrame(np.where(pivot_movie_genre != 0, 1, pivot_movie_genre),
                                            index=pivot_movie_genre.index,
                                            columns=pivot_movie_genre.columns)
        
        pivot_movie_cast = movie_cast.pivot_table(index=['movie_id'], columns=['cast_id'], values=['id'], fill_value=0)
        pivot_movie_cast = pd.DataFrame(np.where(pivot_movie_cast != 0, 1, pivot_movie_cast),
                                            index=pivot_movie_cast.index,
                                            columns=pivot_movie_cast.columns)
        
        pivot_movie_production_company = movie_production_company.pivot_table(index=['movie_id'], columns=['production_company_id'], values=['id'], fill_value=0)
        pivot_movie_production_company = pd.DataFrame(np.where(pivot_movie_production_company != 0, 1, pivot_movie_production_company),
                                            index=pivot_movie_production_company.index,
                                            columns=pivot_movie_production_company.columns)
        
        pivot_movie_production_country = movie_production_country.pivot_table(index=['movie_id'], columns=['production_country_id'], values=['id'], fill_value=0)
        pivot_movie_production_country = pd.DataFrame(np.where(pivot_movie_production_country != 0, 1, pivot_movie_production_country),
                                            index=pivot_movie_production_country.index,
                                            columns=pivot_movie_production_country.columns)

        pivot_movie_spoken_languages = movie_spoken_languages.pivot_table(index=['movie_id'], columns=['spoken_language_id'], values=['id'], fill_value=0)
        pivot_movie_spoken_languages = pd.DataFrame(np.where(pivot_movie_spoken_languages != 0, 1, pivot_movie_spoken_languages),
                                        index=pivot_movie_spoken_languages.index,
                                        columns=pivot_movie_spoken_languages.columns)

        # recommend movies based on other users
        # user-based
        user_rating_pivot = user_rating[['user_id', 'movie_id', 'rating_score']].pivot_table(index=['user_id'], columns=['movie_id'], values='rating_score')
        user_rating_pivot.fillna(0, inplace=True)
        user_movie_rating = scaler.fit_transform(user_rating_pivot)

        movie_user_rating = user_movie_rating.T

        user_similarity = cosine_similarity(user_movie_rating)

        temp1 = user_similarity.dot(user_movie_rating)
        user_based_predict = (temp1/np.column_stack([user_similarity.sum(axis=1)] * temp1.shape[-1])).T
        
        # item-based
        df_words = movie['overview'] + movie['tagline'] + movie['title']
        df_words = df_words.apply(lambda x: x.lower())

        ps = PorterStemmer()
        def stem(text):
            y = []

            for i in text.split():
                y.append(ps.stem(i))

            return " ".join(y)
        df_words.apply(stem)

        cv = CountVectorizer(max_features=1000, stop_words='english')
        vectors = cv.fit_transform(df_words).toarray()

        word_sim = cosine_similarity(vectors)

        genre_sim = cosine_similarity(pivot_movie_genre)

        cast_sim = cosine_similarity(pivot_movie_cast)

        company_sim = cosine_similarity(pivot_movie_production_company)

        country_sim = cosine_similarity(pivot_movie_production_country)

        language_sim = cosine_similarity(pivot_movie_spoken_languages)

        metric_df = movie[['budget', 'release_date', 'runtime', 'popularity', 'rating_score', 'view_count']]
        
        current_date = datetime.now().date()
        metric_df.loc[:,'release_date'] = (current_date - metric_df['release_date']).apply(lambda x: x.days)

        metric_normalize = scaler.fit_transform(metric_df)
        metric_sim = cosine_similarity(metric_normalize)
        #print(word_sim.shape)
        # print(genre_sim.shape)
        # print(cast_sim.shape)
        # print(company_sim.shape)
        # print(country_sim.shape)
        # print(language_sim.shape)
        # print(metric_sim.shape)
        #print(movie_user_rating.shape)

        movie_similarity = (30*word_sim + 6*genre_sim + 20*cast_sim + company_sim + country_sim + language_sim + metric_sim)/60

        temp2 = movie_similarity.dot(movie_user_rating)
        item_based_predict = temp2/np.column_stack([movie_similarity.sum(axis=1)] * temp2.shape[-1])

        collaborative_filtering = (item_based_predict + user_based_predict)/2
        collaborative_filtering = pd.DataFrame(collaborative_filtering, index=user_rating_pivot.columns, columns=user_rating_pivot.index)

        # recommend movies based on user
        # content-based 

        user_genre = view_history.merge(movie_genre, on='movie_id')[['user_id', 'genre_id']]
        user_genre_pivot = user_genre.pivot_table(index='user_id', columns='genre_id', aggfunc='size', fill_value=0)
        user_genre_normalize = scaler.fit_transform(user_genre_pivot)
        item_user_sim_genre = cosine_similarity(np.vstack((user_genre_normalize, pivot_movie_genre)))[len(user_genre_normalize):, :len(user_genre_normalize)]

        user_country = view_history.merge(movie_production_country, on='movie_id')[['user_id', 'production_country_id']]
        user_country_pivot = user_country.pivot_table(index='user_id', columns='production_country_id', aggfunc='size', fill_value=0)
        user_country_normalize = scaler.fit_transform(user_country_pivot)
        # print(user_country_normalize.shape)
        # print(pivot_movie_production_country.shape)
        item_user_sim_country = cosine_similarity(np.vstack((user_country_normalize, pivot_movie_production_country)))[len(user_country_normalize):, :len(user_country_normalize)]

        user_company = view_history.merge(movie_production_company, on='movie_id')[['user_id', 'production_company_id']]
        user_company_pivot = user_company.pivot_table(index='user_id', columns='production_company_id', aggfunc='size', fill_value=0)
        user_company_normalize = scaler.fit_transform(user_company_pivot)
        item_user_sim_company = cosine_similarity(np.vstack((user_company_normalize, pivot_movie_production_company)))[len(user_company_normalize):, :len(user_company_normalize)]

        user_language = view_history.merge(movie_spoken_languages, on='movie_id')[['user_id', 'spoken_language_id']]
        user_language_pivot = user_language.pivot_table(index='user_id', columns='spoken_language_id', aggfunc='size', fill_value=0)
        user_language_normalize = scaler.fit_transform(user_language_pivot)
        item_user_sim_language = cosine_similarity(np.vstack((user_language_normalize, pivot_movie_spoken_languages)))[len(user_language_normalize):, :len(user_language_normalize)]

        content_based_predict = (item_user_sim_company + item_user_sim_country + item_user_sim_genre + item_user_sim_language) / 4
        content_based_predict = pd.DataFrame(content_based_predict, index=user_rating_pivot.columns, columns=user_rating_pivot.index)

        # update model 
        for user_ids in content_based_predict.columns:

            user = User.objects.get(id=user_ids)

            a = set(view_history[view_history.user_id == user_ids]['movie_id'].values)
            b = content_based_predict.loc[:,user_ids].sort_values(ascending=False).index
            c = collaborative_filtering.loc[:,user_ids].sort_values(ascending=False).index

            result_list_content = [item for item in b if item not in a]
            result_list_collborative = [item for item in c if item not in a]

            for movie_ids in result_list_collborative[:10]:
                movie = Movie.objects.get(id=movie_ids)
                UserRecommendModel.objects.create(user=user, movie=movie, recommend_score = content_based_predict.loc[movie_ids, user_ids])

            for movie_ids in result_list_content[:10]:
                movie = Movie.objects.get(id=movie_ids)
                PersonalRecommendModel.objects.create(user=user, movie=movie, recommend_score = collaborative_filtering.loc[movie_ids, user_ids])
    
                
