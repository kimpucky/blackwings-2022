# Generated by Django 3.2.7 on 2021-10-09 21:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]