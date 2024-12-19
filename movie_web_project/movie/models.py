from django.db import models
from django.db.models import Count
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=100)
    profile_path = models.URLField(blank=True, null=True)

class Genre(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    actors = models.ManyToManyField(Actor, related_name='acted_in_movies')
    genres = models.ManyToManyField(Genre, related_name='movies_in_genre')
    description = models.TextField(max_length=10000, blank=True, null=True)
    
    release_date = models.DateField(blank=True, null=True)
    
    duration = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)

    
    def update_view_count(self):
        view_count = View_history.objects.filter(movie=self).aggregate(total_views=Count('id'))['total_views']
        self.view_count = view_count
        self.save()

    def update_rating_score(self):
        avg_rating = User_rating.objects.filter(movie=self).aggregate(avg_rating=Avg('rating_score'))['avg_rating']
        self.rating_score = avg_rating
        self.save()

class View_history(models.Model):
    view_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class User_rating(models.Model):
    rating_score = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10),])
    rating_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)