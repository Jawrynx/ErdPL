# Generated by Django 5.1.4 on 2025-01-15 13:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_team_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='num_weeks',
            field=models.IntegerField(default=22),
        ),
        migrations.AddField(
            model_name='division',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
