# Generated by Django 3.2.7 on 2022-02-05 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment_commentdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='seller',
            new_name='donor',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='buyer',
            new_name='requestor',
        ),
    ]
