# Generated by Django 4.2.6 on 2023-11-13 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_event_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(upload_to='images/events/%y/%m/%d/'),
        ),
    ]
