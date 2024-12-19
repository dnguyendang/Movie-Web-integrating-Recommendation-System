# Generated by Django 4.2.5 on 2023-11-16 21:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0004_alter_movie_casts_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_rating',
            name='rating_score',
            field=models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]