from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from Movie.models import Movie
# Create your models here.

countries = [('CANADA', 'CANADA'),
             ('USA', 'USA'),
             ('UK', 'UK'),
             ('GERMANY', 'GERMANY'),
             ('FRANCE', 'FRANCE'),
             ('OTHER', 'OTHER'),
             ('RUSSIA', 'RUSSIA'), 
             ('VIETNAM', 'VIETNAM'), 
             ('CHINA', 'CHINA')]

class InfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length = 10, choices=[('Male','Male'), ('Female','Female'), ('Other', 'Other')], blank=True, null=True)
    country = models.CharField(max_length = 50, choices=countries, blank=True, null=True)

# model recommendation system
class PersonalRecommendModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    recommend_score = models.FloatField(blank=True, null=True)

class UserRecommendModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    recommend_score = models.FloatField(blank=True, null=True)


