# Generated by Django 4.2.5 on 2023-10-11 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_rating',
            name='rating_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='view_history',
            name='view_time',
            field=models.DateTimeField(),
        ),
    ]