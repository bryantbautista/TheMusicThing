# Generated by Django 4.2.6 on 2023-12-07 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicThing', '0004_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('CommentID', models.AutoField(primary_key=True, serialize=False)),
                ('AlbumID', models.CharField(max_length=22)),
                ('Username', models.CharField(max_length=30)),
                ('Text', models.TextField()),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
