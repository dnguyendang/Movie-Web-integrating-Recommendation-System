from django_cron import CronJobBase, Schedule
from .models import Movie, Genre, Cast, User_rating, Spoken_language, Production_company, Production_country, View_history
from django.db.models import Count

class UpdatePopularityCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # once a day
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Movie.update_popularity_cron_job'

    def do(self):
        movies = Movie.objects.all()
        for movie in movies:
            movie.update_rating_score()
            movie.update_view_count()
            movie.update_popularity()

        # Genre.link_to_other_genre()
        #Cast.link_to_unidentified_cast()
        #Spoken_language.link_to_unidentified_languague()
        #Production_country.link_to_unidentified_country()
        #Production_company.link_to_unidentified_company()

        # unrated_movies = Movie.objects.annotate(num_ratings=Count('user_rating')).filter(num_ratings=0)
        # # Lặp qua danh sách các movie chưa được rating và tạo các User_rating mới với rating_score = 0 và user_id = 1
        # for movie in unrated_movies:
        #     User_rating.objects.create(rating_score=0, user_id=1, movie=movie)

        # # Lấy danh sách các movie chưa được xem bởi user nào
        # unviewed_movies = Movie.objects.annotate(num_views=Count('view_history')).filter(num_views=0)

        # # Lặp qua danh sách các movie chưa được xem và tạo các view_history mới với user_id = 1
        # for movie in unviewed_movies:
        #     View_history.objects.create(user_id=1, movie=movie)