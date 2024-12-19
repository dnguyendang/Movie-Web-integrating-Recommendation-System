import os
import django
import pandas as pd
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_project2.settings")
django.setup()

from django.contrib.auth.models import User
from Account.models import UserProfile

# df = pd.read_csv('users.csv')

# for index, row in df.iterrows():
#     username = row['username']
#     email = row['email']
#     first_name = row['firstname']
#     last_name = row['lastname']
#     password = row['password']
#     gender = row['Sex']
#     birth_date = row['birth_date']

#     user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)

#     profile = UserProfile(user=user, gender=gender, birth_date=birth_date)
#     profile.save()

rating_df = pd.read_csv('ratings_small.csv')
name = pd.read_csv('username.csv', index_col=0)

for user_id in set(rating_df['userId']):
    if user_id == 1:
        continue
    User.objects.filter(id=user_id).delete()

    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    birth_date = fake.date_of_birth()
    gender = fake.random_element(['male', 'female'])
    username = name.iloc[user_id]
    email = fake.email()
    password = fake.password()

    user = User.objects.create(id = user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    profile = UserProfile(user=user, gender=gender, birth_date=birth_date)
    profile.save()

