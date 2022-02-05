# Generated by Django 4.0.2 on 2022-02-05 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20220205_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_donor',
            field=models.BooleanField(default=False, verbose_name='donor status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_requestor',
            field=models.BooleanField(default=False, verbose_name='requestor status'),
        ),
    ]