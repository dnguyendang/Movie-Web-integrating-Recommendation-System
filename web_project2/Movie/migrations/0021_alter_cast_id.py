# Generated by Django 4.2.5 on 2024-03-03 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0020_movie_casts_movie_genres_movie_production_companies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
