# Generated by Django 4.2.6 on 2023-11-15 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MusicThing', '0002_alter_ratings_albumid_delete_albums'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Artists',
        ),
        migrations.DeleteModel(
            name='Genres',
        ),
    ]
