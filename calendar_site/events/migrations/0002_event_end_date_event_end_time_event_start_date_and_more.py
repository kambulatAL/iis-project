# Generated by Django 4.2.6 on 2023-10-18 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-01-01'),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='12:30'),
        ),
    ]