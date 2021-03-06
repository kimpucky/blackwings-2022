# Generated by Django 4.0.2 on 2022-02-05 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_donor_alter_user_is_donor_requesting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_donor',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_requestor',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_requestor', models.BooleanField(default=False, verbose_name='requestor status')),
                ('is_donor', models.BooleanField(default=True, verbose_name='donor status')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmed')),
                ('address', models.CharField(blank=True, max_length=512, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=50, verbose_name='State')),
                ('zipcode', models.DecimalField(blank=True, decimal_places=0, max_digits=5, verbose_name='Zipcode')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
