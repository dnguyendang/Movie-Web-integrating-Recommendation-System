# Generated by Django 4.2.5 on 2024-03-02 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_userrecommendmodel_personalrecommendmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalrecommendmodel',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='personalrecommendmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userrecommendmodel',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='userrecommendmodel',
            name='user',
        ),
    ]
