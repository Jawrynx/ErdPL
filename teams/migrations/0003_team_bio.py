# Generated by Django 5.1.1 on 2025-01-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_team_team_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='bio',
            field=models.TextField(blank=True),
        ),
    ]
