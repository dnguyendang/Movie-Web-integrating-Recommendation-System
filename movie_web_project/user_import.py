import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE","movie_web_project.settings")
django.setup()

from django.contrib.auth.models import User
from userprofile.models import UserProfile

df = pd.read_csv('users.csv')

for index, row in df.iterrows():
    username = row['username']
    email = row['email']
    first_name = row['firstname']
    last_name = row['lastname']
    password = row['password']
    gender = row['Sex']
    birth_date = row['birth_date']

    user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)

    profile = UserProfile(user=user, gender=gender, birth_date=birth_date)
    profile.save()