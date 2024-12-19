from django.db import models
from django.db.models import Avg, Count, Max, Min
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Cast(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    gender = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_path = models.URLField(blank=True, null=True)
    
    @staticmethod
    def link_to_unidentified_cast():
        # Lấy ra genre có tên 'other' hoặc tạo mới nếu không tồn tại
        unidentified_cast, _ = Cast.objects.get_or_create(name='Unidentified')

        # Lấy ra tất cả các movie không có liên kết với bất kỳ cast nào
        movies_without_cast = Movie.objects.filter(casts=None)

        # Liên kết mỗi movie không có genre với genre 'other'
        for movie in movies_without_cast:
            movie.casts.add(unidentified_cast)

class Genre(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    @staticmethod
    def link_to_other_genre():
        # Lấy ra genre có tên 'other' hoặc tạo mới nếu không tồn tại
        other_genre, _ = Genre.objects.get_or_create(name='other')

        # Lấy ra tất cả các movie không có liên kết với bất kỳ genre nào
        movies_without_genre = Movie.objects.filter(genres=None)

        # Liên kết mỗi movie không có genre với genre 'other'
        for movie in movies_without_genre:
            movie.genres.add(other_genre)

class Production_company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    origin_country = models.CharField(max_length=100, blank=True, null=True)
    logo_path = models.URLField(blank=True, null=True)
    @staticmethod
    def link_to_unidentified_company():
        # Lấy ra genre có tên 'other' hoặc tạo mới nếu không tồn tại
        unidentified_company, _ = Production_company.objects.get_or_create(name='Unidentified')

        # Lấy ra tất cả các movie không có liên kết với bất kỳ cast nào
        movies_without_companies = Movie.objects.filter(production_companies=None)

        # Liên kết mỗi movie không có genre với genre 'other'
        for movie in movies_without_companies:
            movie.casts.add(unidentified_company)

class Production_country(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    iso_3166_1 = models.CharField(max_length=100, blank=True, null=True)
    @staticmethod
    def link_to_unidentified_country():
        # Lấy ra genre có tên 'other' hoặc tạo mới nếu không tồn tại
        unidentified_country, _ = Production_country.objects.get_or_create(name='Unidentified')

        # Lấy ra tất cả các movie không có liên kết với bất kỳ cast nào
        movies_without_cast = Movie.objects.filter(production_countries=None)

        # Liên kết mỗi movie không có genre với genre 'other'
        for movie in unidentified_country:
            movie.casts.add(unidentified_country)

class Spoken_language(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    iso_639_1 = models.CharField(max_length=100, blank=True, null=True)
    @staticmethod
    def link_to_unidentified_languague():
        # Lấy ra genre có tên 'other' hoặc tạo mới nếu không tồn tại
        unidentified_languague, _ = Spoken_language.objects.get_or_create(name='Unidentified')

        # Lấy ra tất cả các movie không có liên kết với bất kỳ cast nào
        movies_without_language = Movie.objects.filter(spoken_languages=None)

        # Liên kết mỗi movie không có genre với genre 'other'
        for movie in movies_without_language:
            movie.casts.add(unidentified_languague)

class Movie(models.Model):
    backdrop_path = models.URLField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    overview = models.TextField(max_length=10000, blank=True, null=True)
    poster_path = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    revenue = revenue = models.BigIntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    tagline = models.TextField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    vote_average = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    trailer_link = models.URLField(blank=True, null=True)
    rating_score = models.FloatField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)

    spoken_languages = models.ManyToManyField(Spoken_language, related_name='spoken_in_movies')
    production_companies = models.ManyToManyField(Production_company, related_name='movies_producted_by')
    production_countries = models.ManyToManyField(Production_country, related_name='movies_in_country')
    casts = models.ManyToManyField(Cast, related_name='acted_in_movies')
    genres = models.ManyToManyField(Genre, related_name='movies_in_genre')

    def update_view_count(self):
        view_count = View_history.objects.filter(movie=self).aggregate(total_views=Count('id'))['total_views']
        self.view_count = view_count
        self.save()

    def update_rating_score(self):
        avg_rating = User_rating.objects.filter(movie=self).aggregate(avg_rating=Avg('rating_score'))['avg_rating']
        if avg_rating is None:
            self.rating_score = 0
        else:
            self.rating_score = avg_rating
        self.save()

    def update_popularity(self):
        #normalize rating_score 
        max_view_count = Movie.objects.aggregate(Max('view_count'))['view_count__max']
        min_view_count = Movie.objects.aggregate(Min('view_count'))['view_count__min']
        norm_view_count = (self.view_count - min_view_count)/(max_view_count - min_view_count)

        max_release_date = Movie.objects.aggregate(Max('release_date'))['release_date__max']
        min_release_date = Movie.objects.aggregate(Min('release_date'))['release_date__min'] 
        norm_release_date = (self.release_date - min_release_date)/(max_release_date - min_release_date)
        
        popularity_score = self.rating_score + norm_view_count*10 + norm_release_date*100
        self.popularity = popularity_score
        self.save()

class View_history(models.Model):
    view_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

class User_rating(models.Model):
    rating_score = models.IntegerField(default=0, blank=True, null=True)
    rating_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)