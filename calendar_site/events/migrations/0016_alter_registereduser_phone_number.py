# Generated by Django 4.2.6 on 2023-11-23 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_remove_eventestimation_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
