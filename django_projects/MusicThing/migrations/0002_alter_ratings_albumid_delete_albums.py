# Generated by Django 4.2.6 on 2023-11-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicThing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='AlbumID',
            field=models.CharField(max_length=22),
        ),
        migrations.DeleteModel(
            name='Albums',
        ),
    ]
