# Generated by Django 4.2.6 on 2023-12-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicThing', '0003_delete_artists_delete_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
