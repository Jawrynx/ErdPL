# Generated by Django 5.1.4 on 2025-02-27 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0006_alter_individualscore_away_player_and_more'),
        ('users', '0009_player_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualscore',
            name='away_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='away_scores', to='users.player'),
        ),
        migrations.AlterField(
            model_name='individualscore',
            name='home_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_scores', to='users.player'),
        ),
    ]
