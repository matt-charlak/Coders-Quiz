# Generated by Django 2.2.12 on 2023-05-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180331_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
