# Generated by Django 2.2.12 on 2023-05-20 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_game_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='description',
            new_name='description1',
        ),
    ]
