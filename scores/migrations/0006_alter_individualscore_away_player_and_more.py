# Generated by Django 5.1.4 on 2025-02-20 15:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0005_remove_individualscore_away_player_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualscore',
            name='away_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='away_scores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='individualscore',
            name='home_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_scores', to=settings.AUTH_USER_MODEL),
        ),
    ]
