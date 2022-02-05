# Generated by Django 3.2.7 on 2021-10-09 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist_inwatchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='inWatchList',
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
