from django.db import models

# Create your models here.
class Artists(models.Model):
    ArtistID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    def __str__(self):
        return self.Name

class Genres(models.Model):
    GenreID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)

class Albums(models.Model):
    AlbumID = models.AutoField(primary_key=True)
    ArtistID = models.ForeignKey(Artists, on_delete=models.CASCADE)
    GenreID = models.ForeignKey(Genres, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    ReleaseDate = models.DateField(auto_now=False, auto_now_add=False)
    LengthMins = models.IntegerField()
    Rating = models.DecimalField(max_digits=3, decimal_places=2)

class Ratings(models.Model):
    RatingID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=30)
    AlbumID = models.ForeignKey(Albums, on_delete=models.CASCADE)
    Rating = models.IntegerField()

