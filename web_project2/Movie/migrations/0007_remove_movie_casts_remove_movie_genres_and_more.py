# Generated by Django 4.2.5 on 2023-11-17 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0006_alter_user_rating_rating_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='casts',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='production_companies',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='production_countries',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='spoken_languages',
        ),
        migrations.RemoveField(
            model_name='user_rating',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='user_rating',
            name='user',
        ),
        migrations.RemoveField(
            model_name='view_history',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='view_history',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cast',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.DeleteModel(
            name='Production_company',
        ),
        migrations.DeleteModel(
            name='Production_country',
        ),
        migrations.DeleteModel(
            name='Spoken_language',
        ),
        migrations.DeleteModel(
            name='User_rating',
        ),
        migrations.DeleteModel(
            name='View_history',
        ),
    ]
