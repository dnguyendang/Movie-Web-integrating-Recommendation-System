# Generated by Django 4.2.5 on 2023-11-15 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('profile_path', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backdrop_path', models.URLField(blank=True, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, max_length=10000, null=True)),
                ('poster_path', models.URLField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('revenue', models.BigIntegerField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('tagline', models.TextField(blank=True, max_length=1000, null=True)),
                ('title', models.CharField(max_length=200)),
                ('vote_average', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('trailer_link', models.URLField(blank=True, null=True)),
                ('casts', models.ManyToManyField(blank=True, null=True, related_name='acted_in_movies', to='Movie.cast')),
                ('genres', models.ManyToManyField(blank=True, null=True, related_name='movies_in_genre', to='Movie.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Production_company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Production_country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Spoken_language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='View_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_score', models.DecimalField(decimal_places=2, max_digits=3)),
                ('rating_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='production_companies',
            field=models.ManyToManyField(blank=True, null=True, related_name='movies_producted_by', to='Movie.production_company'),
        ),
        migrations.AddField(
            model_name='movie',
            name='production_countries',
            field=models.ManyToManyField(blank=True, null=True, related_name='movies_in_country', to='Movie.production_country'),
        ),
        migrations.AddField(
            model_name='movie',
            name='spoken_languages',
            field=models.ManyToManyField(blank=True, null=True, related_name='spoken_in_movies', to='Movie.spoken_language'),
        ),
    ]
