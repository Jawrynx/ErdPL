# Generated by Django 5.1.4 on 2025-01-01 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_nickname_customuser_fullname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='nickname',
            new_name='fullname',
        ),
    ]
