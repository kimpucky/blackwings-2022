# Generated by Django 3.2.7 on 2021-10-09 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211008_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='inWatchList',
            field=models.BooleanField(default=False),
        ),
    ]
