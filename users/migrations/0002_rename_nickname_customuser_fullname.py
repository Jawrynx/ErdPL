# Generated by Django 5.1.4 on 2025-01-01 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='nickname',
            new_name='fullname',
        ),
    ]
